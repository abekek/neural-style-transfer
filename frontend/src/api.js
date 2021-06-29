import axios from "axios";

const baseUrl = "https://ux344irjs6.execute-api.us-east-2.amazonaws.com/dev/transform";

function transform(data) {
  return axios.post(baseUrl, data);
}

export { transform };