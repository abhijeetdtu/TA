Vue.component('board-members', {
  props:['memberDetails'],
  template: `<div>
  <p class="h3"> Current Board </p>
  <div class="row">
    <div class="col" v-for="member in memberDetails">
      <board-member-info
        v-bind:name="member.name"
        v-bind:title="member.title"
        v-bind:email="member.email"
        v-bind:imgurl="member.imgurl"
        v-bind:intro="member.intro"
        ></board-member-info>
    </div>
  </div>
  </div>
  `
})
