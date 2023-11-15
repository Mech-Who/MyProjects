import seaborn as sn
import matplotlib.pyplot as plt

for fold in config["train_folds"]:
    metrics = pd.read_csv(f"/kaggle/working/logs_f{fold}/lightning_logs/version_0/metrics.csv")
    del metrics["step"]
    del metrics["lr"]
    del metrics["train_loss_step"]
    metrics.set_index("epoch", inplace=True)
    g = sn.relplot(data=metrics, kind="line")
    plt.title(f"Fold {fold}")
    plt.gcf().set_size_inches(15, 5)
    plt.grid()
    plt.show()
