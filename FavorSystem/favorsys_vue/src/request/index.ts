import axios from "axios";
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";

// eslint-disable-next-line
interface FSRequestConfig extends AxiosRequestConfig {}

class FSRequest {
  instance: AxiosInstance;
  constructor(config: FSRequestConfig) {
    this.instance = axios.create(config);
  }
  request<T>(config: FSRequestConfig): Promise<AxiosResponse<T>> {
    return new Promise((resolve, reject) => {
      this.instance
        .request<T>(config)
        .then((res) => {
          resolve(res);
        })
        .catch((err) => {
          reject(err);
          return err;
        });
    });
  }
}

export default FSRequest;
