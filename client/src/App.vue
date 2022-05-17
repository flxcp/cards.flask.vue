<template>
  <div class="h-100" id="app">
    <nav>
      <NavBar />
    </nav>
    <div class="mt-4 h-100">
      <router-view />
    </div>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";

export default {
  components: {
    NavBar,
  },
};
</script>

<style>
#app,
body,
html {
  background-color: #e6e6fa;
}
</style>
