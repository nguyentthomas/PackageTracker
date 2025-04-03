import { fetchUtils, DataProvider, GetListParams, GetManyParams } from "react-admin";

const apiUrl = "http://localhost:8000";
const httpClient = fetchUtils.fetchJson;

const dataProvider: DataProvider = {
  getList: async (resource, params) => {
    const { page, perPage } = params.pagination;
    const filters = params.filter ? `&filter=${encodeURIComponent(JSON.stringify(params.filter))}` : "";
    const url = `${apiUrl}/${resource}?page=${page}&perPage=${perPage}${filters}`;
    const { json } = await httpClient(url);

    return {
      data: json.data,
      total: json.total,
    }
  },
  
  getOne: async (resource, params) => {
    const url = `${apiUrl}/${resource}/${params.id}`;
    const { json } = await httpClient(url);
    return { data: json };
  },

  create: async (resource, params) => {
    const response = await fetch(`${apiUrl}/${resource}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(params.data),
    });

    const json = await response.json();
    if (!response.ok) throw new Error(json.detail || "Error creating resource");

    return { data: json.data };  // ✅ Ensure `data` is returned properly
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