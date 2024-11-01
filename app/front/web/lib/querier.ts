// const url: string = "http://127.0.0.1";
// const port: number = 8081;

// async function query(
//   method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
//   path = "/",
//   body = {},
//   token = ""
// ): Promise<any> {
//   try {
//     const payload: RequestInit = {
//       method: method,
//       mode: "cors",
//       headers: {
//         'Content-Type': 'application/json'
//       }
//     };

//     if (token !== "") {
//       (payload.headers as HeadersInit)["Authorization"] = `Bearer ${token}`;
//     }

//     if (method !== "GET" && Object.keys(body).length > 0) {
//       payload.body = JSON.stringify(body);
//     }

//     if (port === -1) {
//       const final_url = `${url}${path}`;
//     } else {
//       const final_url = `${url}:${port}${path}`;
//     }
//     const response: Response = await fetch(final_url, payload);

//     if (!response.ok) {
//       throw new Error(`Error: ${response.status}`);
//     }

//     const data = await response.json();
//     return data;
//   } catch (error) {
//     console.error('Error fetching data:', error);
//     throw error;
//   }
// }

// async function get(path = "/", body: object = {}, token = ""): Promise<any> {
//   return await query("GET", path, body, token);
// }

// async function put(path = "/", body: object = {}, token = ""): Promise<any> {
//   return await query("PUT", path, body, token);
// }

// async function post(path = "/", body: object = {}, token = ""): Promise<any> {
//   return await query("POST", path, body, token);
// }

// async function delete_query(path = "/", body: object = {}, token = ""): Promise<any> {
//   return await query("DELETE", path, body, token);
// }

// const queries = {
//   query,
//   get,
//   put,
//   post,
//   delete_query
// };

// export { queries };

// const url = "http://127.0.0.1";
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
    console.log(final_url);
    console.log(payload);
    const response: Response = await fetch(final_url, payload);
    console.log(response);
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    console.log(response);
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
