Vue.component('events-list', {
  props:['events'],
  template: `<div>
  <p class="h3"> Events </p>
  <div class="row">
    <div class="col" v-for="event in events">
        <b-card
          v-bind:title="event.title"
          v-bind:img-src="event.imgurl"
          img-alt="Image"
          img-top
          tag="article"
          style="max-width: 10rem;"
          class="mb-2"
        >
          <b-card-text>
            <div class="row">
              {{event.date}}
            </div>
            <div class="row"> {{event.url}} </div>

          </b-card-text>
        </b-card>
    </div>
  </div>
  </div>
  `
})
