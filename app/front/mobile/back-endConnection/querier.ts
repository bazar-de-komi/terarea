const url: string = "https://ifttt-back.pingpal.news";
const port: number = -1;

async function query(
  method: "GET" | "POST" | "PATCH" | "PUT" | "DELETE" = "GET",
  path: string = "/",
  body: object = {},
  token: string = ""
): Promise<any> {
  try {
    const payload: RequestInit = {
      method: method,
      mode: "cors",
      headers: {
        'Content-Type': 'application/json'
      }
    };

    if (token !== "") {
      (payload.headers as HeadersInit)["Authorization"] = `Bearer ${token}`;
    }

    if (method !== "GET" && Object.keys(body).length > 0) {
      payload.body = JSON.stringify(body);
    }

    let final_url: string;

    if (port === -1) {
      final_url = `${url}${path}`;
    } else {
      final_url = `${url}:${port}${path}`;
    }
    const response: Response = await fetch(final_url, payload);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    throw error;
  }
}

async function get(path: string = "/", body: object = {}, token: string = ""): Promise<any> {
  return await query("GET", path, body, token);
}

async function put(path: string = "/", body: object = {}, token: string = ""): Promise<any> {
  return await query("PUT", path, body, token);
}

async function post(path: string = "/", body: object = {}, token: string = ""): Promise<any> {
  return await query("POST", path, body, token);
}

async function patch(path: string = "/", body: object = {}, token: string = ""): Promise<any> {
  return await query("PATCH", path, body, token);
}

async function delete_query(path: string = "/", body: object = {}, token: string = ""): Promise<any> {
  return await query("DELETE", path, body, token);
}

const queries = {
  query,
  get,
  put,
  post,
  patch,
  delete_query
};

export { queries };
