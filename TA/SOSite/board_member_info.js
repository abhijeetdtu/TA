Vue.component('board-member-info', {
  props:['name' , 'title' , 'email'  , 'imgurl' , 'intro'],
  template: `<div>
    <b-card
      v-bind:title="name"
      v-bind:img-src="imgurl"
      img-alt="Image"
      img-top
      tag="article"
      style="max-width: 20rem;"
      class="mb-2"
    >
      <b-card-text>
        <hr/>
        <div class="row">
          {{title}}
        </div>
        <hr/>
        <div class="row"> {{email}} </div>
        <hr/>
        <div class="row">
          {{intro}}
        </div>
      </b-card-text>
    </b-card>
  </div>
  `
})
