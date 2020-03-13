<template>
  <div id="search">

    <form>
      <input type="text" placeholder="Search for Package .." spellcheck="false"
             @input.prevent="onInputText" :value="text">

      <select @change.prevent="onChange" v-model="classifier">
        <option value="" selected>- Classifier auswählen -</option>
        <option v-for="classifier in classifiers">
          {{classifier}}
        </option>
      </select>

      <select @change.prevent="onChangeSize" v-model="size">
        <option>10</option>
        <option selected>20</option>
        <option>50</option>
        <option>100</option>
      </select>
    </form>

    <h2>Results:</h2>
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Version</th>
          <th>Summary</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in result.batch">
          <td><a :href="item.project_url" :title="item.description">{{item.name}}</a></td>
          <td>{{item.version}}</td>
          <td>{{item.summary}}</td>
        </tr>
      </tbody>
    </table>

    <hr>
    <button @click.prevent="prevPage">Previous</button>
    <button @click.prevent="nextPage">Next</button>
    <span>Page: {{page}} / {{totalPages}}</span>

  </div>
</template>

<script>
  import settings from '../settings'
  import axios from 'axios'

  export default {
    name   : 'Search',
    data(){
      return {
        text: '',
        classifier: '',
        start: 0,
        page: 1,
        totalPages: 1,
        size: 20,
        default_classiers: [
          'Framework :: Plone',
        ],
        versions: [
          {"Framework :: Plone :: 4.3": "4.3"},
          {"Framework :: Plone :: 5.0": "5.0"},
          {"Framework :: Plone :: 5.1": "5.1"},
          {"Framework :: Plone :: 5.2": "5.2"}
        ],
        type: ["Addon", "Core", "Theme"],
        classifiers: [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Plone :: 4.3',
          'Framework :: Plone :: 5.0',
          'Framework :: Plone :: 5.1',
          'Framework :: Plone :: 5.2',
          'Framework :: Plone :: Addon',
          'Framework :: Zope2',
          'Framework :: Zope3',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.7',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries :: Python Modules'
        ], // Random Classifier for temporary Testing
        result: []
      }
    },
    created(){
      this.loadSearchResults()
    },
    methods: {
      loadSearchResults: function() {
        let params = {
          text: this.text,
          classifier: this.classifier,
          start: this.start,
          size: this.size
        };
        axios
          .post(settings.api_url + '?' + this.dictToURI(params))
          .then(response => {
            this.result = response.data.result;
            this.start = this.result.start;
            this.totalPages = Math.ceil(this.result.total / this.size);
          })
          .catch(e => {
            this.errors.push(e)
          })
      },
      onInputText: function (event) {
        this.text = event.target.value;
        this.start = 0;
        this.page = 1;
        this.loadSearchResults()
      },
      onChange: function (event) {
        this.start = 0;
        this.page = 1;
        this.loadSearchResults()
      },
      onChangeSize: function (event) {
        this.size = parseInt(event.target.value);
        this.onChange()
      },
      nextPage: function () {
        if (this.start + this.size < this.result.total) {
          this.start += this.size;
          this.page++;
          this.loadSearchResults()
        }
      },
      prevPage: function () {
        if (this.page > 1) {
          this.start -= this.size;
          this.page--;
          this.loadSearchResults()
        }
      },
      dictToURI: function (dict) {
        let str = [];
        for(let key in dict) {
          if (dict[key]) {
            str.push(
              encodeURIComponent(key) + "=" +
              encodeURIComponent(dict[key]));
          }
        }
        return str.join("&");
      }
    }
  }
</script>

<style scoped>

</style>
