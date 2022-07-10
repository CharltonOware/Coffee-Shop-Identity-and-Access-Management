
export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-ozv6oy4k.us', // the auth0 domain prefix
    audience: 'coffeeview', // the audience set for the auth0 app
    clientId: 'Ux30hPyPfjPiu6Yg8JAWdo2jYmiLl8tQ', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
