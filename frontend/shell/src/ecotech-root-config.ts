import { registerApplication, start, LifeCycles } from "single-spa";

// registerApplication({
//   name: "@single-spa/welcome",
//   app: () =>
//     import(
//       /* webpackIgnore: true */ // @ts-ignore-next
//       "https://unpkg.com/single-spa-welcome/dist/single-spa-welcome.js"
//     ),
//   activeWhen: (location) => location.pathname === "/",
// });

registerApplication({
  name: "@ecotech/login-mfe",
  app: () =>
    import(
      /* webpackIgnore: true */ // @ts-ignore-next
      "@ecotech/login-mfe"
    ),
  activeWhen: (location) => location.pathname === "/",
});

registerApplication({
  name: "@ecotech/orders-mfe",
  app: () =>
    import(
      /* webpackIgnore: true */ // @ts-ignore-next
      "@ecotech/orders-mfe"
    ),
  activeWhen: (location) => location.pathname === "/orders",
});

start({
  urlRerouteOnly: true,
});
