import FSRequest from "@/request";

const BASE_URL = "http://localhost:8888";
const TIME_OUT = 10000;

const fsRequest = new FSRequest({
  baseURL: BASE_URL,
  timeout: TIME_OUT,
});

export default fsRequest;
