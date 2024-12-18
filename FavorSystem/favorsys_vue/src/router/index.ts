import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "root",
    redirect: "/home",
  },
  {
    path: "/home",
    name: "home",
    component: () =>
      import(/* webpackChunkName: "home" */ "../views/HomeView.vue"),
  },
  {
    path: "/about",
    name: "about",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/manage",
    name: "manage",
    redirect: "/manage/people",
    component: () =>
      import(/* webpackChunkName: "manage" */ "../components/ManageLayout.vue"),
    children: [
      {
        path: "/people",
        name: "people",
        component: () =>
          import(/* webpackChunkName: "people" */ "../views/PeopleView.vue"),
      },
      {
        path: "/people/:peopleId",
        name: "people_info",
        // props: true,
        component: () =>
          import(
            /* webpackChunkName: "people" */ "../views/PeopleInfoView.vue"
          ),
      },
      {
        path: "/event",
        name: "event",
        component: () =>
          import(/* webpackChunkName: "event" */ "../views/EventView.vue"),
      },
    ],
  },
  {
    path: "/404",
    name: "404",
    component: () =>
      import(/* webpackChunkName: "404" */ "../components/NotFound.vue"),
  },
  {
    path: "/:pathMath(.*)",
    meta: {
      hidden: true,
    },
    redirect: "/404",
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
