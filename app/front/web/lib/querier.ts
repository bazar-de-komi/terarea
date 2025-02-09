const url = "https://ifttt-back.pingpal.news";
const port = -1;

async function query(
  method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE" = "GET",
  path = "/",
  body = {},
  token = ""
): Promise<any> {
  try {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const payload: RequestInit = {
      method: method,
      mode: "cors",
      headers: headers,
    };

    if (method !== "GET" && Object.keys(body).length > 0) {
      payload.body = JSON.stringify(body);
    }

    let final_url: string;

    if (port === -1) {
      final_url = `${url}${path}`;
    } else {
      final_url = `${url}:${port}${path}`;
    }
    console.log("Final URL:", final_url);
    console.log("Payload:", payload);
    const response: Response = await fetch(final_url, payload);
    console.log(response);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}

async function get(path = "/", body: object = {}, token = ""): Promise<any> {
  return await query("GET", path, body, token);
}

async function put(path = "/", body: object = {}, token = ""): Promise<any> {
  return await query("PUT", path, body, token);
}

async function post(path = "/", body: object = {}, token = ""): Promise<any> {
  return await query("POST", path, body, token);
}

async function patch(path = "/", body = {}, token = ""): Promise<any> {
  return await query("PATCH", path, body, token);
}

async function delete_query(path = "/", body = {}, token = ""): Promise<any> {
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
