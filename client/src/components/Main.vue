<template>
<v-container>
  <v-data-table
    :headers="headers"
    :items="content"
    sort-by="calories"
    class="elevation-1" >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Tags</v-toolbar-title>
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="mb-2" v-on="on">New Item</v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.id" label="ID"
                      :rules="[() => !!editedItem.id || 'This field is required']">
                    </v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-select
                      ref="type"
                      v-model="editedItem.type"
                      :rules="[() => !!editedItem.type || 'This field is required']"
                      :items="['artist', 'album', 'track']"
                      label="Type"
                      required
                    ></v-select>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.tags"
                      :rules="[() => !!editedItem.tags || 'This field is required']"
                      label="tag1, tag2, ..."></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.action="{ item }">

      <v-icon
        small
        @click="deleteItem(item)"
      >
        delete
      </v-icon>
    </template>
  </v-data-table>

    <v-row>
      <v-card-title>Search content by tags</v-card-title>
    </v-row>
    <v-row>
      <v-col cols="12" sm="2" md="2">
      <v-select
        ref="type"
        v-model="search_tag.type"
        :rules="[() => !!search_tag.type || 'This field is required']"
        :items="['artist', 'album', 'track']"
        label="Type"
        required
      ></v-select>
      </v-col>
      <v-col cols="12" sm="2" md="2">
        <v-text-field v-model="search_tag.tags"
          :rules="[() => !!search_tag.tags || 'This field is required']" label="tag1, tag2, ...">
        </v-text-field>
      </v-col>
      <v-col cols="12" sm="2" md="2">
        <v-btn color="primary" dark class="mb-2" @click="searchtags">
          Search tags
        </v-btn>
      </v-col>
    </v-row>
    <v-data-table
      :headers='headers_search'
      :items='tags_search'
      :items-per-page='10'
      class='elevation-1'
    ></v-data-table>
  </v-container>
</template>
<script>
import axios from 'axios';

export default {
  name: 'Crud',
  data: () => ({
    dialog: false,
    headers: [
      {
        text: 'ID',
        align: 'left',
        sortable: false,
        value: 'id',
      },
      { text: 'Type', value: 'type' },
      { text: 'Tags', value: 'tags' },
      { text: 'Actions', value: 'action', sortable: false },
    ],
    headers_search: [
      {
        text: 'ID',
        align: 'left',
        sortable: false,
        value: 'id',
      },
      { text: 'Type', value: 'type' },
      { text: 'Tags', value: 'tags' },
    ],
    content: [],
    editedIndex: -1,
    editedItem: {
      id: '',
      type: '',
      tags: '',
    },
    defaultItem: {
      id: '',
      type: '',
      tags: '',
    },
    search_tag: {
      type: '',
      tags: '',
    },
    tags_search: [],
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item';
    },
  },

  watch: {
    dialog(val) {
      // eslint-disable-next-line
      val || this.close();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      const path = 'http://localhost:5000/export';
      axios.get(path)
        .then((res) => {
          this.content = res.data.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
            console.error(error);
        });
    },

    editItem(item) {
      this.editedIndex = this.content.indexOf(item);
      this.editedItem = { ...item };
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.content.indexOf(item);
      // eslint-disable-next-line
      const confirmation = confirm('Are you sure you want to delete this item?');
      if (confirmation) {
        const path = `http://localhost:5000/${this.content[index].type}/${this.content[index].id}`;
        axios.delete(path)
          .then((res) => {
            console.log(res);
          })
          .catch((error) => {
            // eslint-disable-next-line
                  console.error(error);
          });
        if (this.content.length === 1) {
          this.content = [];
        } else {
          this.content.splice(index, 1);
        }
      }
    },

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.editedItem = { ...this.defaultItem };
        this.editedIndex = -1;
      }, 300);
    },

    save() {
      if (this.editedItem.id && this.editedItem.type && this.editedItem.tags) {
        const tagsToSave = this.editedItem.tags.split(',').map((ell) => ell.trim());
        this.editedItem.tags = tagsToSave;
        if (this.editedIndex > -1) {
          Object.assign(this.content[this.editedIndex], this.editedItem);
        } else {
          this.content.push(this.editedItem);
        }
        const path = `http://localhost:5000/${this.editedItem.type}/${this.editedItem.id}`;
        axios.post(path, tagsToSave)
          .then((res) => {
            console.log(res);
          })
          .catch((error) => {
            // eslint-disable-next-line
                  console.error(error);
          });
        this.close();
      }
    },
    searchtags() {
      if (this.search_tag.type && this.search_tag.tags) {
        const path = `http://localhost:5000/${this.search_tag.type}`;
        const tagsToSearch = this.search_tag.tags.split(',').map((ell) => ell.trim());
        axios.get(path, { params: { tags: tagsToSearch } })
          .then((res) => {
            this.tags_search = res.data.data;
          })
          .catch((error) => {
            // eslint-disable-next-line
                  console.error(error);
          });
      }
    },
  },
};
</script>

<style scoped>

</style>
