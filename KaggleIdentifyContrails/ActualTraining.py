# Actual training
import warnings
warnings.filterwarnings("ignore")
import gc
import os
import torch
import yaml
import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping, TQDMProgressBar
from torch.utils.data import DataLoader
from sklearn.model_selection import KFold
from pytorch_lightning.loggers import CSVLogger

torch.set_float32_matmul_precision("medium")
with open("config.yaml", "r") as file_obj:
    config = yaml.safe_load(file_obj)
pl.seed_everything(config["seed"])
gc.enable()
contrails = os.path.join(config["data_path"], "contrails/")
train_path = os.path.join(config["data_path"], "train_df.csv")
valid_path = os.path.join(config["data_path"], "valid_df.csv")

train_df = pd.read_csv(train_path)
valid_df = pd.read_csv(valid_path)

train_df["path"] = contrails + train_df["record_id"].astype(str) + ".npy"
valid_df["path"] = contrails + valid_df["record_id"].astype(str) + ".npy"

df = pd.concat([train_df, valid_df]).reset_index()

Fold = KFold(shuffle=True, **config["folds"])
for n, (trn_index, val_index) in enumerate(Fold.split(df)):
    df.loc[val_index, "kfold"] = int(n)
df["kfold"] = df["kfold"].astype(int)

for fold in config["train_folds"]:
    print(f"\n###### Fold {fold}")
    trn_df = df[df.kfold != fold].reset_index(drop=True)
    vld_df = df[df.kfold == fold].reset_index(drop=True)
    dataset_train = ContrailsDataset(trn_df, config["model"]["image_size"], train=True)
    dataset_validation = ContrailsDataset(vld_df, config["model"]["image_size"], train=False)
    data_loader_train = DataLoader(
        dataset_train,
        batch_size=config["train_bs"],
        shuffle=True,
        num_workers=config["workers"],
    )
    data_loader_validation = DataLoader(
        dataset_validation,
        batch_size=config["valid_bs"],
        shuffle=False,
        num_workers=config["workers"],
    )
    checkpoint_callback = ModelCheckpoint(
        save_weights_only=True,
        monitor="val_dice",
        dirpath=config["output_dir"],
        mode="max",
        filename=f"model-f{fold}-{{val_dice:.4f}}",
        save_top_k=1,
        verbose=1,
    )
    progress_bar_callback = TQDMProgressBar(
        refresh_rate=config["progress_bar_refresh_rate"]
    )
    early_stop_callback = EarlyStopping(**config["early_stop"])

    trainer = pl.Trainer(
        callbacks=[checkpoint_callback, early_stop_callback, progress_bar_callback],
        logger=CSVLogger(save_dir=f'logs_f{fold}/'),
        **config["trainer"],
    )
    model = LightningModule(config["model"])
    trainer.fit(model, data_loader_train, data_loader_validation)

    del (
        dataset_train,
        dataset_validation,
        data_loader_train,
        data_loader_validation,
        model,
        trainer,
        checkpoint_callback,
        progress_bar_callback,
        early_stop_callback,
    )
    torch.cuda.empty_cache()
    gc.collect()
