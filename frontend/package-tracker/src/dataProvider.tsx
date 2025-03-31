import { fetchUtils, DataProvider, GetListParams } from "react-admin";

const apiUrl = "http://localhost:8000/packages/";
const httpClient = fetchUtils.fetchJson;

const dataProvider: DataProvider = {
  getList: async (resource, params: GetListParams) => {
    const url = `${apiUrl}/${resource}`;
    const { json } = await httpClient(url);
    return { data: json, total: json.length };
  },

  getOne: async (resource, params) => {
    const url = `${apiUrl}/${resource}/${params.id}`;
    const { json } = await httpClient(url);
    return { data: json };
  },

  create: async (resource, params) => {
    const url = `${apiUrl}/${resource}`;
    const { json } = await httpClient(url, {
      method: "POST",
      body: JSON.stringify(params.data),
    });
    return { data: json };
  },

  update: async (resource, params) => {
    const url = `${apiUrl}/${resource}/${params.id}`;
    const { json } = await httpClient(url, {
      method: "PUT",
      body: JSON.stringify(params.data),
    });
    return { data: json };
  },

  delete: async (resource, params) => {
    const url = `${apiUrl}/${resource}/${params.id}`;
    await httpClient(url, { method: "DELETE" });
    return { data: params.previousData };
  },
};


export default dataProvider;