export function inProduction() {
  return import.meta.env.MODE !== 'development'
}
