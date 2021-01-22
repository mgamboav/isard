<template>
  <div>
    <b-container fluid>
      <!-- Button view -->
      <transition-group v-if="gridView" appear name="bounce">
        <!-- Persistent desktops -->
        <b-row v-if="persistent" key="persistent" align-h="center">
          <b-card v-for="desktop in desktops" :key="desktop.id" class="shadow persistent_desktop m-3 border-secondary" no-body>
            <b-card-body>
              <font-awesome-icon size="4x" :icon="icons[desktop.icon]" class="mb-2"/>
              <b-card-title><h6>{{ desktop.name }}</h6></b-card-title>
              <b-card-sub-title class="mb-2">
                <small>{{status[desktop.state.toLowerCase()].text}}</small>
              </b-card-sub-title>
              <!-- Viewers button/drowpdown -->
              <span v-if="desktop.state.toLowerCase() == 'started'">
                <b-button variant="primary" class="m-1" v-if="desktop.viewers.length === 1"
                @click="openDesktop({desktopId: desktop.id, viewer: desktop.viewers[0]})">
                  {{desktop.viewers[0]}}
                </b-button>
                <b-dropdown v-else variant="primary"
                :text="$t('views.select-template.viewers')" class="m-1">
                  <b-dropdown-item v-for="viewer in desktop.viewers" :key="viewer" @click="openDesktop({desktopId: desktop.id, viewer: viewer})">{{viewer}}</b-dropdown-item>
                </b-dropdown>
              </span>
              <!-- Change status button -->
              <b-button :variant="status[desktop.state.toLowerCase()].variant" class="m-1"
               @click="changeDesktopStatus({ action: status[desktop.state.toLowerCase()].action, desktopId: desktop.id })">
                <font-awesome-icon :icon="status[desktop.state.toLowerCase()].icon" class="mr-2"/>
                {{status[desktop.state.toLowerCase()].actionText}}
              </b-button>
            </b-card-body>
            <b-card-footer>
              <small><b>{{$t('views.select-template.template')}}:</b> {{desktop.template}}</small>
            </b-card-footer>
          </b-card>
        </b-row>
        <!-- Non persistent desktops -->
        <b-row v-else key="nonpersistent" align-h="center">
          <b-card v-for="desktop in desktops" :key="desktop.id" class="shadow temporal_desktop m-3" no-body>
            <b-card-body>
              <b-row no-gutters>
                <b-col cols="4">
                  <font-awesome-icon class="mt-2" size="4x" :icon="icons[desktop.icon]" />
                </b-col>
                <b-col cols="8">
                  <b-card-title><h6>{{ desktop.name }}</h6></b-card-title>
                  <b-card-sub-title class="mb-2" v-if="desktop.state">
                    <small>{{status[desktop.state.toLowerCase()].text}}</small>
                  </b-card-sub-title>
                  <!-- If the desktop is executing we can use its viewers or delete it -->
                  <span v-if="desktop.state">
                    <b-button variant="primary" class="m-1" v-if="desktop.viewers.length === 1"
                    @click="openDesktop({desktopId: desktop.id, viewer: desktop.viewers[0]})">
                      {{desktop.viewers[0]}}
                    </b-button>
                    <b-dropdown v-else variant="primary" size="sm"
                    :text="$t('views.select-template.viewers')" class="m-1">
                      <b-dropdown-item v-for="viewer in desktop.viewers" :key="viewer" @click="openDesktop({desktopId: desktop.id, viewer: viewer})">{{viewer}}</b-dropdown-item>
                    </b-dropdown>
                    <b-button variant="danger" size="sm" @click="deleteDesktop(desktop.id)">
                      <font-awesome-icon :icon="['fas', 'trash']" class="mr-2"/>
                      {{ $t('views.select-template.remove') }}
                    </b-button>
                  </span>
                  <!-- Otherwise we can create it using the template id -->
                  <b-button v-else size="sm" :variant="status.stopped.variant"  @click="chooseDesktop(desktop.id)">
                    <font-awesome-icon :icon="status.stopped.icon" class="mr-2"/>
                    {{status.stopped.actionText}}
                  </b-button>
                </b-col>
              </b-row>
            </b-card-body>
            <b-card-footer>
              <small><b>{{$t('views.select-template.template')}}:</b> {{desktop.template ? desktop.template : desktop.id}}</small>
            </b-card-footer>
          </b-card>
        </b-row>
      </transition-group>
      <!-- Table view -->
      <b-row v-else>
        <b-table v-if="persistent" :items="desktops" :fields="table_fields"
        id="desktops-table" class="text-left" key="desktops_table">
          <!-- Persistent desktops -->
          <template #cell(action)="data">
            <b-button :variant="status[data.item.state.toLowerCase()].variant"
            @click="changeDesktopStatus({action: status[data.item.state.toLowerCase()].action, desktopId: data.item.id})">
              <font-awesome-icon :icon="status[data.item.state.toLowerCase()].icon" class="mr-2"/>
              {{status[data.item.state.toLowerCase()].actionText}}
            </b-button>
          </template>
          <template #cell(viewers)="data">
            <b-dropdown v-if="data.item.state.toLowerCase() == 'started'" variant="primary"
            :text="$t('views.select-template.viewers')">
              <b-dropdown-item v-for="viewer in data.item.viewers" :key="viewer" @click="openDesktop({desktopId: data.item.id, viewer: viewer})">{{viewer}}</b-dropdown-item>
            </b-dropdown>
          </template>
          <template #cell(name)="data">
            <col style="width: 10cm" class="d-flex align-items-center">
              <font-awesome-icon :icon="icons[data.item.icon]" size="2x" class="mr-2"/>
              {{ data.item.name }}
            <col>
          </template>
        </b-table>
          <b-table v-else :items="desktops" :fields="table_fields"
          id="desktops-table" class="text-left" key="desktops_table">
          <!-- Non persistent desktops -->
          <template #cell(action)="data">
            <b-button v-if="data.item.state" variant="danger" @click="removeDesktop()">
              <font-awesome-icon :icon="['fas', 'trash']" class="mr-2"/>
              {{ $t('views.select-template.remove') }}
            </b-button>
            <b-button v-else :variant="status.stopped.variant"  @click="chooseDesktop(data.item.id)">
              <font-awesome-icon :icon="status.stopped.icon" class="mr-2"/>
              {{status.stopped.actionText}}
            </b-button>
          </template>
          <template #cell(viewers)="data">
            <b-dropdown v-if="data.item.state && data.item.state.toLowerCase() == 'started'" variant="primary"
            :text="$t('views.select-template.viewers')">
              <b-dropdown-item v-for="viewer in data.item.viewers" :key="viewer" @click="openDesktop({desktopId: data.item.id, viewer: viewer})">{{viewer}}</b-dropdown-item>
            </b-dropdown>
          </template>
          <template #cell(name)="data">
            <col style="width: 10cm" class="d-flex align-items-center">
              <font-awesome-icon :icon="icons[data.item.icon]" size="2x" class="mr-2"/>
              {{ data.item.name }}
            <col>
          </template>
          <template #cell(status)="data">
            <span v-if="data.item.state">{{status[data.item.state.toLowerCase()].text}}</span>
          </template>
        </b-table>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// @ is an alias to /src
import i18n from '@/i18n'
import { mapActions } from 'vuex'

export default {
  props: {
    desktops: {
      required: true,
      type: Array
    },
    gridView: {
      required: true,
      type: Boolean
    },
    persistent: {
      required: true,
      type: Boolean
    },
    icons: {
      required: true,
      type: Object
    },
    status: {
      required: true,
      type: Object
    }
  },
  methods: {
    ...mapActions([
      'openDesktop',
      'deleteDesktop',
      'changeDesktopStatus'
    ]),
    chooseDesktop (template) {
      const data = new FormData()
      data.append('template', template)
      this.$store.dispatch('createDesktop', data)
    }
  },
  data () {
    return {
      table_fields: [
        {
          key: 'action',
          label: i18n.t('components.desktop-cards.table-header.action')
        },
        {
          key: 'viewers',
          label: i18n.t('components.desktop-cards.table-header.viewers')
        },
        {
          key: 'state',
          sortable: true,
          formatter: value => {
            return value ? this.status[value.toLowerCase()].text : ''
          },
          sortByFormatted: true,
          label: i18n.t('components.desktop-cards.table-header.state')
        },
        {
          key: 'name',
          sortable: true,
          label: i18n.t('components.desktop-cards.table-header.name')
        },
        {
          key: 'description',
          sortable: true,
          label: i18n.t('components.desktop-cards.table-header.description')
        }
      ]
    }
  }
}
</script>

<style scoped>

  .persistent_desktop {
    min-height:250px !important;
    min-width:400px !important;
    z-index: 0 !important;
  }

  .temporal_desktop {
    min-height:100px !important;
    min-width:350px !important;
    z-index: 0 !important;
  }

  .card:hover{
    z-index: 1 !important;
    box-shadow: 8px 8px 5px blue;
    transform: scale(1.1);
  }

  .bounce-enter-active {
    animation: bounce-in .5s;
  }
  .bounce-leave-active {
    animation: bounce-in .5s reverse;
  }
  @keyframes bounce-in {
    0% {
      transform: scale(0);
    }
    50% {
      transform: scale(1.5);
    }
    100% {
      transform: scale(1);
    }
  }
</style>
