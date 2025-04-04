import { AxiosError, type AxiosInstance, type InternalAxiosRequestConfig } from 'axios'
import axios from 'axios'

export interface LoginApiResponse {
  access: string
  refresh: string
}

export type RefreshApiResposne = Pick<LoginApiResponse, 'access'>

interface ExtendedInternalAxiosRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean
}

/**
 * Checks whether the application in prodcution mode
 */
export function inProduction() {
  return process.env.NODE_ENV !== 'development'
}

/**
 * A function used in order to get the correct domain
 * to which a request should be sent (Django, Quart or Flask)
 *
 * @param altDomain Production domain used if inProduction() is true
 * @param [websocket=false] Create a domain for websocket connection
 * @param [port=8000] Change the default port
 */
export function getDomain(altDomain?: string | null | undefined, websocket: boolean = false, port: number = 8000): string {
  let domain = '127.0.0.1'

  if (altDomain && altDomain.startsWith('http')) {
    throw new Error('Domain should not start with http:// or https://')
  }

  if (inProduction()) {
    // Use the alternative domain (which is the production domain)
    // only in production. Locally, we use 127.0.0.1 or localhost
    domain = altDomain || import.meta.env.VITE_PROD_URL
  }

  let loc = websocket ? 'ws' : 'http'
  let url: URL

  if (inProduction()) {
    loc += 's'
  }

  if (!domain) {
    throw new Error('prodDomain or altDomain needs to be specified')
  }

  if (domain && inProduction()) {
    url = new URL(`${loc}://${domain}`)
  } else {
    url = new URL(`${loc}://${domain}:${port}`)
  }

  return url.toString()
}

/**
 * Function that returns an url ready to be used with any Django or Quart
 * websocket endpoint
 *
 * @param path The path to the endpoint to use
 * @param altDomain Alternative odmain to the one registered in useRuntimeConfig.public.prodUrl
 * @param [port=8000] The port of the backend (development only)
 */
export function getWebsocketUrl(path: string, altDomain?: string | null | undefined, port: number = 8000): string {
  const domain = getDomain(altDomain, true, port)
  const url = new URL(path, domain)
  return url.toString()
}

/**
 * Function used to create a basic axios client that
 * can be used to send api requests
 * 
 * @param altDomain Alternative odmain to the one registered in useRuntimeConfig.public.prodUrl
 * @param [port=8000] The port of the backend (development only)
 */
export function createSimpleClient(altDomain?: string | null | undefined, port: number = 8000) {
  return axios.create({
    baseURL: getDomain(altDomain, false, port),
    withCredentials: true,
    headers: { 'Content-Type': 'application/json' },
    timeout: 10000
  })
}

/**
 * Function that adds authentication intercepors on the base client
 * in order to send and handle authenticated requests
 * 
 * @param client The client to decorate with the intereceptors
 * @param access Access token
 * @param refresh Refresh token
 * @param refreshCallback Callback function used to return the refresh token
 * @param errorCallback Callback function used on error
 */
function authenticationInterceptors(client: AxiosInstance, access?: string | null | undefined, refresh?: string | null | undefined, refreshCallback?: (token: string) => void, errorCallback?: (error: AxiosError) => void) {
  client.interceptors.request.use(
    (config) => {
      if (access) {
        config.headers.Authorization = `Token ${access}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  client.interceptors.response.use(
    (response) => {
      return response
    },
    async (error: AxiosError) => {
      // Sequence that refreshes the access token when
      // we get a 401 code trying to access a page

      const originalRequest = error.config as ExtendedInternalAxiosRequestConfig

      if (error.response) {
        if (error.response.status === 401 && !originalRequest?._retry) {
          originalRequest._retry = true

          try {
            const authClient = axios.create({ baseURL: getDomain() })
            const response = await authClient.post<RefreshApiResposne>('/auth/v1/refresh', { refresh })

            if (refreshCallback) {
              refreshCallback(response.data.access)
            }

            return authClient
          } catch (refreshError) {
            if (errorCallback && refreshError instanceof AxiosError) {
              errorCallback(refreshError)
            }
            return Promise.reject(refreshError)
          }
        }
      }

      return Promise.reject(error)
    }
  )

  return client
}

/**
 * Composable used to get an Axios instance on the client side.
 * It allows us to invoke composables such as "useCookies" from
 * vueuse and other composables that require client sotrages to
 * be fully available
 * 
 * @param altDomain Production domain used if inProduction() is true
 * @param [port=8000] Change the default port
 */
export function useAxiosClient(altDomain?: string | null | undefined, port: number = 8000) {
  const client = createSimpleClient(altDomain, port)
  const authenticatedClient = authenticationInterceptors(client)

  return {
    client,
    authenticatedClient
  }
}

/**
 * Same as useAxiosClient but adds a layer of authentication
 * that with access and refresh tokens for protected views
 * 
 * @param access Access token
 * @param refresh Refresh token
 * @param altDomain Production domain used if inProduction() is true
 * @param [port=8000] Change the default port
 */
export function useAuthenticatedAxiosClient(access: string | null | undefined, refresh: string | null | undefined, altDomain?: string | null | undefined, port: number = 8000) {
  const { client } = useAxiosClient(altDomain, port)
  const authenticatedClient = authenticationInterceptors(client, access, refresh)

  return {
    authenticatedClient
  }
}
