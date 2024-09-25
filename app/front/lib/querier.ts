// // const url = "http://s-backend";
// const url = "http://127.0.0.1";
// const port = 5000;

// async function query(method = "GET", path = "/", body = {}, token = "") {
//   try {
//     var payload = {
//       method: method,
//       mode: "cors",
//       headers: {
//         'Content-Type': 'application/json'
//       }
//     }
//     if (token !== "") {
//       payload.headers["Authorization"] = `Bearer ${token}`
//     }
//     if (method !== "GET" && Object.keys(body).length > 0) {
//       payload.body = JSON.stringify(body);
//     }
//     const final_url = `${url}:${port}${path}`
//     const response = await fetch(final_url, payload);

//     if (!response.ok) {
//       throw new Error(`Error: ${response.status}`);
//     }

//     const data = await response.json();
//     return data;
//   } catch (error) {
//     console.error('Error fetching data:', error);
//   }
// }

// async function get(path = "/", body = {}, token = "") {
//   return await query("GET", path, body, token)
// }

// async function put(path = "/", body = {}, token = "") {
//   return await query("PUT", path, body, token)
// }

// async function post(path = "/", body = {}, token = "") {
//   return await query("POST", path, body, token)
// }

// async function delete_query(path = "/", body = {}, token = "") {
//   return await query("DELETE", path, body, token)
// }

// const queries = {
//   query,
//   get,
//   put,
//   post,
//   delete_query
// };

// export { queries };

const url: string = "http://127.0.0.1";
const port: number = 5000;

interface QueryOptions {
  method?: string;
  path?: string;
  body?: object;
  token?: string;
}

async function query(
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET", 
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

    const final_url: string = `${url}:${port}${path}`;
    const response: Response = await fetch(final_url, payload);

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

async function get(path: string = "/", body: object = {}, token: string = ""): Promise<any> {
  return await query("GET", path, body, token);
}

async function put(path: string = "/", body: object = {}, token: string = ""): Promise<any> {
  return await query("PUT", path, body, token);
}

async function post(path: string = "/", body: object = {}, token: string = ""): Promise<any> {
  return await query("POST", path, body, token);
}

async function delete_query(path: string = "/", body: object = {}, token: string = ""): Promise<any> {
  return await query("DELETE", path, body, token);
}

const queries = {
  query,
  get,
  put,
  post,
  delete_query
};

export { queries };
