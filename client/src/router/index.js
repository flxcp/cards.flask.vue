import Vue from "vue";
import VueRouter from "vue-router";
import SigninView from "../views/SigninView.vue";
import DashboardView from "../views/DashboardView.vue";
import ProfileView from "../views/ProfileView.vue";
import DeckView from "../views/DeckView.vue";
import CardsView from "../views/CardsView.vue";
import ReviewDeck from "../views/ReviewDeck.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "dashboard",
    component: DashboardView,
  },
  {
    path: "/signin",
    name: "signin",
    component: SigninView,
  },
  {
    path: "/deck",
    name: "deck",
    component: DeckView,
  },
  {
    path: "/deck/:id/cards",
    name: "cards",
    component: CardsView,
  },
  {
    path: "/review/deck/:id",
    name: "review",
    component: ReviewDeck,
  },
  {
    path: "/profile",
    name: "profile",
    component: ProfileView,
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../views/RegisterView"),
  },
  {
    path: "*",
    name: "Error",
    component: () => import("../views/ErrorView"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("auth-token");
  if (token || to.name === "signin" || to.name === "register") {
    next();
  } else {
    next({ name: "signin" });
  }
});

export default router;
