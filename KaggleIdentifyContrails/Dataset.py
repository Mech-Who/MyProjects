# Dataset
import os
import torch
import numpy as np
import pandas as pd
import torchvision.transforms as T

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



if __name__ == '__main__':
    # 创建一个四维张量
    tensor = torch.randn(2, 3, 4, 5)
    # 打印原始维度排列
    print("Original tensor shape:", tensor.shape)  # Output: (2, 3, 4, 5)
    # 使用 permute() 调整维度排列
    tensor_permuted = tensor.permute(0, 2, 3, 1)
    # 打印调整后的维度排列
    print("Permuted tensor shape:", tensor_permuted.shape)  # Output: (2, 4, 5, 3)
