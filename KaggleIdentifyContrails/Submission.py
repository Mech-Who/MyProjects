import warnings
warnings.filterwarnings("ignore")
import gc
import os
import glob
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
import torchvision.transforms as T
import yaml


batch_size = 32
num_workers = 1
THR = 0.5
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
data = './input/google-research-identify-contrails-reduce-global-warming'
data_root = './input/google-research-identify-contrails-reduce-global-warming/test/'
submission = pd.read_csv(os.path.join(data, 'sample_submission.csv'), index_col='record_id')

filenames = os.listdir(data_root)
test_df = pd.DataFrame(filenames, columns = ['record_id'])
test_df['path'] = data_root + test_df['record_id'].astype(str)

class ContrailsDataset(torch.utils.data.Dataset):
    def __init__(self, df, image_size=256, train=True):
        self.df = df
        self.trn = train
        self.df_idx: pd.DataFrame = pd.DataFrame({'idx': os.listdir(f'/kaggle/input/google-research-identify-contrails-reduce-global-warming/test')})
        self.normalize_image = T.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        self.image_size = image_size
        if image_size != 256:
            self.resize_image = T.transforms.Resize(image_size)
    
    def read_record(self, directory):
        record_data = {}
        for x in [
            "band_11", 
            "band_14", 
            "band_15"
        ]:
            record_data[x] = np.load(os.path.join(directory, x + ".npy"))
        return record_data

    def normalize_range(self, data, bounds):
        """Maps data to the range [0, 1]."""
        return (data - bounds[0]) / (bounds[1] - bounds[0])
    
    def get_false_color(self, record_data):
        _T11_BOUNDS = (243, 303)
        _CLOUD_TOP_TDIFF_BOUNDS = (-4, 5)
        _TDIFF_BOUNDS = (-4, 2)
        N_TIMES_BEFORE = 4
        r = self.normalize_range(record_data["band_15"] - record_data["band_14"], _TDIFF_BOUNDS)
        g = self.normalize_range(record_data["band_14"] - record_data["band_11"], _CLOUD_TOP_TDIFF_BOUNDS)
        b = self.normalize_range(record_data["band_14"], _T11_BOUNDS)
        false_color = np.clip(np.stack([r, g, b], axis=2), 0, 1)
        img = false_color[..., N_TIMES_BEFORE]
        return img
    
    def __getitem__(self, index):
        row = self.df.iloc[index]
        con_path = row.path
        data = self.read_record(con_path)    
        img = self.get_false_color(data)
        img = torch.tensor(np.reshape(img, (256, 256, 3))).to(torch.float32).permute(2, 0, 1)
        if self.image_size != 256:
            img = self.resize_image(img) 
        img = self.normalize_image(img)
        image_id = int(self.df_idx.iloc[index]['idx'])    
        return img.float(), torch.tensor(image_id)
    
    def __len__(self):
        return len(self.df)


def rle_encode(x, fg_val=1):
    """
    Args:
        x:  numpy array of shape (height, width), 1 - mask, 0 - background
    Returns: run length encoding as list
    """
    dots = np.where(
        x.T.flatten() == fg_val)[0]  # .T sets Fortran order down-then-right
    run_lengths = []
    prev = -2
    for b in dots:
        if b > prev + 1:
            run_lengths.extend((b + 1, 0))
        run_lengths[-1] += 1
        prev = b
    return run_lengths

def list_to_string(x):
    """
    Converts list to a string representation
    Empty list returns '-'
    """
    if x: # non-empty list
        s = str(x).replace("[", "").replace("]", "").replace(",", "")
    else:
        s = '-'
    return s


class LightningModule(pl.LightningModule):
    def __init__(self, config):
        super().__init__()
        self.model = smp.Unet(encoder_name=config["encoder_name"],
                              encoder_weights=None,
                              in_channels=3,
                              classes=1,
                              activation=None,
                              )
    def forward(self, batch):
        return self.model(batch)

MODEL_PATH = "./working/models/"
with open(os.path.join(MODEL_PATH, "config.yaml"), "r") as file_obj:
    config = yaml.safe_load(file_obj)

test_ds = ContrailsDataset(
        test_df,
        config["model"]["image_size"],
        train = False
    )
test_dl = DataLoader(test_ds, batch_size=batch_size, num_workers = num_workers)


gc.enable()
all_preds = {}

for i, model_path in enumerate(glob.glob(MODEL_PATH + '*.ckpt')):
    print(model_path)
    model = LightningModule(config["model"]).load_from_checkpoint(model_path, config=config["model"])
    model.to(device)
    model.eval()
    model_preds = {}
    for _, data in enumerate(test_dl):
        images, image_id = data
        images = images.to(device)
        with torch.no_grad():
            predicted_mask = model(images[:, :, :, :])
        if config["model"]["image_size"] != 256:
            predicted_mask = torch.nn.functional.interpolate(predicted_mask, size=256, mode='bilinear')
        predicted_mask = torch.sigmoid(predicted_mask).cpu().detach().numpy()     
        for img_num in range(0, images.shape[0]):
            current_mask = predicted_mask[img_num, :, :, :]
            current_image_id = image_id[img_num].item()
            model_preds[current_image_id] = current_mask
    all_preds[f"f{i}"] = model_preds
    del model    
    torch.cuda.empty_cache()
    gc.collect() 


for index in submission.index.tolist():
    for i in range(len(glob.glob(MODEL_PATH + '*.ckpt'))):
        if i == 0:
            predicted_mask = all_preds[f"f{i}"][index]
        else:
            predicted_mask += all_preds[f"f{i}"][index]
    predicted_mask = predicted_mask / len(glob.glob(MODEL_PATH + '*.ckpt'))
    predicted_mask_with_threshold = np.zeros((256, 256))
    predicted_mask_with_threshold[predicted_mask[0, :, :] < THR] = 0
    predicted_mask_with_threshold[predicted_mask[0, :, :] > THR] = 1
    submission.loc[int(index), 'encoded_pixels'] = list_to_string(rle_encode(predicted_mask_with_threshold))

