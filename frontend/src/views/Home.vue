<template>
  <div class="landing-page">
    <header class="landing-header">
      <div class="nav-container">
        <div class="logo-container">
          <img src="/geopulse-logo.svg" alt="GeoPulse" class="nav-logo" />
          <span class="logo-text">GeoPulse</span>
        </div>
        <div class="nav-actions">
          <div class="nav-resource-links" aria-label="Project resources">
            <a
              href="https://tess1o.github.io/geopulse/docs/getting-started/introduction"
              target="_blank"
              rel="noopener noreferrer"
              class="nav-link-pill">
              <i class="pi pi-book"></i>
              <span>Documentation</span>
            </a>
            <a
              href="https://github.com/tess1o/geopulse"
              target="_blank"
              rel="noopener noreferrer"
              class="nav-link-pill">
              <i class="pi pi-github"></i>
              <span>GitHub</span>
            </a>
            <span class="nav-version-badge" aria-label="Current version">{{ navVersionBadge }}</span>
          </div>
          <DarkModeSwitcher class="theme-button" />
          <div class="auth-actions" v-if="!isResolvingAuth">
            <template v-if="authStore.isAuthenticated">
              <Button label="Dashboard" as="router-link" to="/app/timeline" class="nav-btn-primary" size="small" />
              <Button icon="pi pi-sign-out" severity="secondary" text @click="handleSignOut" />
            </template>
            <template v-else>
              <Button v-if="isLoginAvailable" label="Sign In" icon="pi pi-sign-in" as="router-link" to="/login" severity="secondary" text class="nav-signin" />
            </template>
          </div>
        </div>
      </div>
    </header>

    <main class="landing-main">
      <section class="hero-section">
        <div class="hero-container">
          <div class="hero-content">
              <div class="hero-eyebrow">Self-hosted location timeline</div>
            <h1 class="hero-title" v-html="heroTitle"></h1>
            <p class="hero-subtitle" v-if="!isMobileViewport">GeoPulse turns raw GPS points into stays, trips, maps, and insights while your data stays under your control.</p>

            <div class="hero-visual mobile-orbit" v-if="isMobileViewport">
              <div class="visual-showcase">
                <div class="orbit-ring ring-1"></div>
                <div class="orbit-ring ring-2"></div>
                <div class="orbit-ring ring-3"></div>
                <img src="/geopulse-logo.svg" alt="GeoPulse logo" class="massive-logo" />
                <div class="feature-chip chip-1"><div class="chip-icon"><i class="pi pi-send"></i></div><span>Live Tracking</span></div>
                <div class="feature-chip chip-2"><div class="chip-icon"><i class="pi pi-download"></i></div><span>Smart Import</span></div>
                <div class="feature-chip chip-3"><div class="chip-icon"><i class="pi pi-calendar"></i></div><span>Auto-Timeline</span></div>
                <div class="feature-chip chip-4"><div class="chip-icon"><i class="pi pi-chart-line"></i></div><span>Deep Insights</span></div>
                <div class="feature-chip chip-5"><div class="chip-icon"><i class="pi pi-images"></i></div><span>Immich Integration</span></div>
                <div class="feature-chip chip-6"><div class="chip-icon"><i class="pi pi-shield"></i></div><span>SSO and Roles</span></div>
                <div class="feature-chip chip-7"><div class="chip-icon"><i class="pi pi-map-marker"></i></div><span>Geofences</span></div>
              </div>
            </div>
            
            <div class="hero-ctas" v-if="!isResolvingAuth">
              <template v-if="!authStore.isAuthenticated">
                  <div class="hero-actions">
                    <Button label="Start Your Journey" icon="pi pi-arrow-right" iconPos="right" as="router-link" to="/register" size="large" class="btn-hero-primary" />
                    <Button label="Sign In" as="router-link" to="/login" size="large" class="btn-hero-secondary" />
                  </div>

                  <div class="social-proof">
                    <a href="https://github.com/tess1o/geopulse" target="_blank" rel="noopener noreferrer" class="github-badge">
                      <div class="github-icon"><i class="pi pi-github"></i></div>
                      <div class="github-stats">
                        <span class="star-count"><i class="pi pi-star-fill"></i> 700+ Stars</span>
                        <span class="separator">•</span>
                        <span class="fork-count"><i class="pi pi-share-alt"></i> 28+ Forks</span>
                      </div>
                    </a>
                    <p class="social-proof-text">The privacy-first, open-source alternative to Google Timeline.</p>
                  </div>
                </template>
                <template v-else>
                  <div class="hero-actions">
                    <Button label="Go to Dashboard" icon="pi pi-arrow-right" iconPos="right" as="router-link" :to="continueDestination.path" size="large" class="btn-hero-primary" />
                  </div>
                </template>
            </div>
            <div v-else class="loading-auth">
              <i class="pi pi-spin pi-spinner"></i> Loading workspace...
            </div>

          </div>

          <div class="hero-visual" v-if="!isMobileViewport">
            <div class="visual-showcase">
              <div class="orbit-ring ring-1"></div>
              <div class="orbit-ring ring-2"></div>
              <div class="orbit-ring ring-3"></div>
              <img src="/geopulse-logo.svg" alt="GeoPulse logo" class="massive-logo" />
              <div class="feature-chip chip-1"><div class="chip-icon"><i class="pi pi-send"></i></div><span>Live Tracking</span></div>
              <div class="feature-chip chip-2"><div class="chip-icon"><i class="pi pi-download"></i></div><span>Smart Import</span></div>
              <div class="feature-chip chip-3"><div class="chip-icon"><i class="pi pi-calendar"></i></div><span>Auto-Timeline</span></div>
              <div class="feature-chip chip-4"><div class="chip-icon"><i class="pi pi-chart-line"></i></div><span>Deep Insights</span></div>
              <div class="feature-chip chip-5"><div class="chip-icon"><i class="pi pi-images"></i></div><span>Immich Integration</span></div>
              <div class="feature-chip chip-6"><div class="chip-icon"><i class="pi pi-shield"></i></div><span>SSO and Roles</span></div>
              <div class="feature-chip chip-7"><div class="chip-icon"><i class="pi pi-map-marker"></i></div><span>Geofences</span></div>
            </div>
          </div>
        </div>

        <div class="feature-panel-wrapper" v-if="!isResolvingAuth && !authStore.isAuthenticated"
             @mouseenter="stopFeatureAutoPlay"
             @mouseleave="startFeatureAutoPlay">
          <template v-if="isMobileViewport">
            <section class="feature-panel mobile-combined-panel" :class="activeFeature ? activeFeature.colorClass : ''" aria-label="Explore GeoPulse and deployment">
              <div class="feature-panel-header mobile-panel-header">
                <div class="mobile-panel-tab-switch" role="tablist" aria-label="Mobile section tabs">
                  <button
                    type="button"
                    class="mobile-panel-tab"
                    :class="{ active: mobileShowcaseTab === 'features' }"
                    :aria-selected="mobileShowcaseTab === 'features'"
                    @click="mobileShowcaseTab = 'features'">
                    <i class="pi pi-compass"></i>
                    <span>Features</span>
                  </button>
                  <button
                    type="button"
                    class="mobile-panel-tab"
                    :class="{ active: mobileShowcaseTab === 'deployment' }"
                    :aria-selected="mobileShowcaseTab === 'deployment'"
                    @click="mobileShowcaseTab = 'deployment'">
                    <i class="pi pi-server"></i>
                    <span>Deployment</span>
                  </button>
                </div>
              </div>

              <template v-if="mobileShowcaseTab === 'features'">
                <div class="feature-panel-header feature-panel-header-inner">
                  <div class="feature-tabs" role="tablist" aria-label="GeoPulse features">
                    <button
                      v-for="feature in features"
                      :key="feature.id"
                      type="button"
                      class="feature-tab"
                      :class="{ active: activeFeatureId === feature.id }"
                      :aria-selected="activeFeatureId === feature.id"
                      @click="setActiveFeature(feature.id)">
                      <i :class="feature.icon"></i>
                      <span>{{ feature.tabLabel }}</span>
                    </button>
                  </div>
                </div>
                <transition name="fade" mode="out-in">
                  <div v-if="activeFeature" :key="activeFeature.id" class="feature-panel-body">
                    <div class="feature-panel-copy">
                      <h3>{{ activeFeature.title }}</h3>
                      <p>{{ activeFeature.description }}</p>
                      <ul class="feature-highlight-list">
                        <li v-for="point in activeFeature.highlights" :key="point">
                          <i class="pi pi-check-circle"></i>
                          <span>{{ point }}</span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </transition>
              </template>

              <template v-else>
                <div class="deployment-panel-body mobile-deployment-body">
                  <p class="deployment-summary">Self-hosted location tracking and analysis on infrastructure you control.</p>
                  <div class="deployment-chip-grid">
                    <div class="deployment-chip"><i class="pi pi-box"></i><span>Docker</span></div>
                    <div class="deployment-chip"><i class="pi pi-microchip"></i><span>Raspberry Pi</span></div>
                    <div class="deployment-chip"><i class="pi pi-cloud"></i><span>Kubernetes</span></div>
                    <div class="deployment-chip"><i class="pi pi-server"></i><span>Helm</span></div>
                  </div>
                  <ul class="deployment-points">
                    <li><i class="pi pi-check-circle"></i><span>Deploy with Docker Compose or Kubernetes Helm.</span></li>
                    <li><i class="pi pi-check-circle"></i><span>AMD64 and ARM64 support.</span></li>
                    <li><i class="pi pi-check-circle"></i><span>Optional MQTT broker for OwnTracks workflows.</span></li>
                    <li><i class="pi pi-check-circle"></i><span>Images available on Docker Hub and GHCR.</span></li>
                  </ul>
                </div>
              </template>
            </section>
          </template>

          <template v-else>
            <aside class="deployment-panel" aria-label="Platform details">
              <div class="deployment-panel-header">
                <p class="feature-panel-kicker">Deployment Options</p>
              </div>
              <div class="deployment-panel-body">
                <p class="deployment-summary">Self-hosted location tracking and analysis on infrastructure you control.</p>
                <div class="deployment-chip-grid">
                  <div class="deployment-chip"><i class="pi pi-box"></i><span>Docker</span></div>
                  <div class="deployment-chip"><i class="pi pi-microchip"></i><span>Raspberry Pi</span></div>
                  <div class="deployment-chip"><i class="pi pi-cloud"></i><span>Kubernetes</span></div>
                  <div class="deployment-chip"><i class="pi pi-server"></i><span>Helm</span></div>
                </div>
                <ul class="deployment-points">
                  <li><i class="pi pi-check-circle"></i><span>Deploy with Docker Compose or Kubernetes Helm.</span></li>
                  <li><i class="pi pi-check-circle"></i><span>AMD64 and ARM64 support.</span></li>
                  <li><i class="pi pi-check-circle"></i><span>Optional MQTT broker for OwnTracks workflows.</span></li>
                  <li><i class="pi pi-check-circle"></i><span>Images available on Docker Hub and GHCR.</span></li>
                </ul>
              </div>
            </aside>

            <section class="feature-panel" :class="activeFeature ? activeFeature.colorClass : ''" aria-label="Explore GeoPulse">
              <div class="feature-panel-header">
                <p class="feature-panel-kicker">Explore GeoPulse</p>
                <div class="feature-tabs" role="tablist" aria-label="GeoPulse features">
                  <button
                    v-for="feature in features"
                    :key="feature.id"
                    type="button"
                    class="feature-tab"
                    :class="{ active: activeFeatureId === feature.id }"
                    :aria-selected="activeFeatureId === feature.id"
                    @click="setActiveFeature(feature.id)">
                    <i :class="feature.icon"></i>
                    <span>{{ feature.tabLabel }}</span>
                  </button>
                </div>
              </div>
              <transition name="fade" mode="out-in">
                <div v-if="activeFeature" :key="activeFeature.id" class="feature-panel-body">
                  <div class="feature-panel-copy">
                    <h3>{{ activeFeature.title }}</h3>
                    <p>{{ activeFeature.description }}</p>
                    <ul class="feature-highlight-list">
                      <li v-for="point in activeFeature.highlights" :key="point">
                        <i class="pi pi-check-circle"></i>
                        <span>{{ point }}</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </transition>
            </section>
          </template>
        </div>

      </section>

      <section v-if="shouldShowQuickStats" class="quick-stats-section">
        <div class="content-wrapper">
          <div class="quick-stats-grid">
            <article class="quick-stat-tile quick-stat-latest">
              <div class="quick-stat-head"><span class="quick-stat-icon"><i class="pi pi-history"></i></span><p class="quick-stat-label">Latest GPS update</p></div>
              <p class="quick-stat-value">{{ latestGpsUpdateLabel }}</p>
            </article>
            <article class="quick-stat-tile quick-stat-distance">
              <div class="quick-stat-head"><span class="quick-stat-icon"><i class="pi pi-map-marker"></i></span><p class="quick-stat-label">Distance today</p></div>
              <p class="quick-stat-value">{{ distanceTodayLabel }}</p>
            </article>
            <article class="quick-stat-tile quick-stat-moving">
              <div class="quick-stat-head"><span class="quick-stat-icon"><i class="pi pi-send"></i></span><p class="quick-stat-label">Time moving today</p></div>
              <p class="quick-stat-value">{{ timeMovingTodayLabel }}</p>
            </article>
          </div>
        </div>
      </section>
    </main>
    
    <footer class="landing-footer" v-if="!authStore.isAuthenticated">
      <div class="content-wrapper">
        <p>&copy; GeoPulse. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import DarkModeSwitcher from '@/components/DarkModeSwitcher.vue'
import Button from 'primevue/button'
import apiService from '@/utils/apiService'

const router = useRouter()
const authStore = useAuthStore()

const isResolvingAuth = ref(true)
const isLoginAvailable = ref(false)
const isMobileViewport = ref(false)
const continueDestination = ref({ path: '/app/timeline' })
const latestGpsUpdateLabel = ref('')
const distanceTodayLabel = ref('')
const timeMovingTodayLabel = ref('')
const appVersion = ref('')
const mobileShowcaseTab = ref('features')

const activeFeatureId = ref(1)

let featureInterval = null

const startFeatureAutoPlay = () => {
  stopFeatureAutoPlay()
  featureInterval = setInterval(() => {
    const currentIndex = features.findIndex(f => f.id === activeFeatureId.value)
    const nextIndex = (currentIndex + 1) % features.length
    activeFeatureId.value = features[nextIndex].id
  }, 5000)
}

const stopFeatureAutoPlay = () => {
  if (featureInterval) {
    clearInterval(featureInterval)
    featureInterval = null
  }
}

const setActiveFeature = (id) => {
  activeFeatureId.value = id
  startFeatureAutoPlay()
}

const features = [
  {
    id: 1,
    title: 'Real-time Tracking Sources',
    tabLabel: 'Live Tracking',
    description: 'Ingest live points from OwnTracks (HTTP/MQTT), Overland, GPSLogger, Home Assistant, Traccar, and Colota.',
    highlights: ['Supports HTTP and MQTT ingest', 'Low-latency point updates', 'Works with existing mobile trackers'],
    icon: 'pi pi-send',
    colorClass: 'chip-1-color'
  },
  {
    id: 2,
    title: 'Universal Import',
    tabLabel: 'Imports',
    description: 'Bulk import history from Google Timeline, GPX, GeoJSON, OwnTracks exports, and CSV.',
    highlights: ['Bring legacy history in one pass', 'Standard formats supported out of the box', 'Merge old and live data cleanly'],
    icon: 'pi pi-download',
    colorClass: 'chip-2-color'
  },
  {
    id: 3,
    title: 'Smart Timeline Detection',
    tabLabel: 'Timeline',
    description: 'Convert raw points into stays, trips, and gaps with configurable sensitivity and movement logic.',
    highlights: ['Automatic trip and stay grouping', 'Sensitivity tuning for your movement pattern', 'Cleaner timeline with fewer manual edits'],
    icon: 'pi pi-calendar',
    colorClass: 'chip-3-color'
  },
  {
    id: 4,
    title: 'Deep Insights',
    tabLabel: 'Insights + AI',
    description: 'Explore distance, visit frequency, movement patterns, and ask natural-language questions about your travel history.',
    highlights: ['Distance and frequency analytics', 'Behavior patterns over time', 'AI assistant via your OpenAI-compatible API key'],
    icon: 'pi pi-chart-line',
    colorClass: 'chip-4-color'
  },
  {
    id: 5,
    title: 'Immich Integration',
    tabLabel: 'Immich',
    description: 'Show Immich photos directly on your map and timeline to connect places with memories.',
    highlights: ['Photos plotted on map context', 'Moments tied to places and trips', 'Works with self-hosted media flow'],
    icon: 'pi pi-images',
    colorClass: 'chip-5-color'
  },
  {
    id: 6,
    title: 'Sharing, Roles, and SSO',
    tabLabel: 'SSO & Roles',
    description: 'Use friend visibility controls, secure guest links, invitations, audit logs, and OIDC login.',
    highlights: ['Role-based access controls', 'OIDC sign-in for managed teams', 'Safe sharing with guest visibility rules'],
    icon: 'pi pi-shield',
    colorClass: 'chip-6-color'
  },
  {
    id: 7,
    title: 'Geofences and Events',
    tabLabel: 'Geofences',
    description: 'Build smarter geofence automations in minutes, not hours.',
    highlights: ['One rule can cover multiple people or devices', 'Faster event review with powerful filters and quick actions', 'Template setup with clear defaults, preview, and connection testing'],
    icon: 'pi pi-map-marker',
    colorClass: 'chip-7-color'
  }
]

const activeFeature = computed(() => features.find(f => f.id === activeFeatureId.value))

const heroTitle = computed(() => {
  return authStore.isAuthenticated ? 'Welcome back' : 'Self-Host Anywhere'
})

const shouldShowQuickStats = computed(() => {
  return authStore.isAuthenticated && !isResolvingAuth.value
})

const navVersionBadge = computed(() => {
  if (!appVersion.value) {
    return 'v...'
  }
  if (appVersion.value === 'Unknown') {
    return 'Unknown'
  }
  return `v${appVersion.value}`
})

const handleSignOut = async () => {
  await authStore.logout()
  router.push('/')
}

const updateViewportState = () => {
  isMobileViewport.value = window.innerWidth < 768
}

const updateUserStats = () => {
  latestGpsUpdateLabel.value = '2 minutes ago'
  distanceTodayLabel.value = '12.4 km'
  timeMovingTodayLabel.value = '45 min'
}

const fetchVersion = async () => {
  try {
    if (window.VUE_APP_CONFIG && window.VUE_APP_CONFIG.VERSION) {
      appVersion.value = window.VUE_APP_CONFIG.VERSION
    } else {
      const response = await apiService.get('/version')
      appVersion.value = response?.version || 'Unknown'
    }
  } catch (error) {
    appVersion.value = 'Unknown'
  }
}

onMounted(async () => {
  updateViewportState()
  window.addEventListener('resize', updateViewportState)
  fetchVersion()
  
  try {
    await authStore.resolveAuthentication()
    isLoginAvailable.value = authStore.loginAvailable
  } finally {
    isResolvingAuth.value = false
  }
  
  if (authStore.isAuthenticated) {
    updateUserStats()
  }

  if (!authStore.isAuthenticated) {
    startFeatureAutoPlay()
  }
})

onBeforeUnmount(() => {
  stopFeatureAutoPlay()
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', updateViewportState)
  }
})
</script>

<style scoped>
:root {
  --home-bg: #eef4fb;
  --home-card-bg: #ffffff;
  --home-border: #d8e4f0;
  --home-text-primary: #0f172a;
  --home-text-secondary: #52627a;
  --home-accent: #0f766e;
  --home-shadow: 0 10px 30px rgba(14, 30, 57, 0.08);
  --home-hero-gradient: linear-gradient(140deg, #f4f8ff 0%, #edf7f4 45%, #eaf3ff 100%);
  --home-hero-glow: radial-gradient(ellipse at 75% 10%, rgba(37, 99, 235, 0.14) 0%, rgba(37, 99, 235, 0) 62%);
}

* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; overflow-x: hidden; }

.landing-page { position: relative; background: radial-gradient(circle at 8% 10%, #dbeafe 0%, rgba(219, 234, 254, 0) 34%), radial-gradient(circle at 90% 75%, #dcfce7 0%, rgba(220, 252, 231, 0) 30%), var(--home-bg); min-height: 100vh; display: flex; flex-direction: column; overflow-x: hidden; }
.landing-header { background: rgba(244, 248, 255, 0.78); border-bottom: 1px solid var(--home-border); padding: 0.75rem 0; position: sticky; top: 0; z-index: 100; backdrop-filter: blur(10px); }
.nav-container { max-width: 1400px; margin: 0 auto; padding: 0 1.5rem; display: flex; justify-content: space-between; align-items: center; }
.logo-container { display: flex; align-items: center; gap: 0.75rem; }
.nav-logo { height: 32px; width: auto; }
.logo-text { font-size: 1.1rem; font-weight: 700; color: var(--home-text-primary); letter-spacing: -0.02em; }
.nav-actions { display: flex; align-items: center; gap: 1rem; }
.auth-actions { display: flex; align-items: center; gap: 0.5rem; }
.theme-button { display: inline-flex; }
.theme-button :deep(.p-button) {
  width: 2rem;
  height: 2rem;
  border-radius: 0.65rem;
  border: 1px solid rgba(203, 213, 225, 0.9);
  background: rgba(255, 255, 255, 0.75);
  color: #475569;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
}
.theme-button :deep(.p-button:hover) {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(148, 163, 184, 0.95);
  color: #1e293b;
}
.nav-resource-links { display: inline-flex; align-items: center; gap: 0.45rem; }
.nav-link-pill { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.36rem 0.66rem; border-radius: 999px; border: 1px solid rgba(203, 213, 225, 0.85); background: rgba(255, 255, 255, 0.7); color: var(--home-text-secondary); text-decoration: none; font-size: 0.79rem; font-weight: 600; transition: all 0.2s ease; }
.nav-link-pill i { font-size: 0.8rem; }
.nav-link-pill:hover { color: #1e293b; border-color: rgba(148, 163, 184, 0.95); background: rgba(255, 255, 255, 0.95); transform: translateY(-1px); }
.nav-version-badge { display: inline-flex; align-items: center; padding: 0.3rem 0.56rem; border-radius: 999px; border: 1px solid rgba(203, 213, 225, 0.9); background: rgba(255, 255, 255, 0.96); color: #7c3aed; font-size: 0.76rem; font-weight: 700; letter-spacing: 0.03em; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06); }

@media (max-width: 1200px) {
  .nav-link-pill span { display: none; }
  .nav-link-pill { padding: 0.38rem; width: 2rem; justify-content: center; }
}

@media (max-width: 980px) {
  .nav-version-badge { display: none; }
  .nav-resource-links { gap: 0.35rem; }
}

@media (max-width: 860px) {
  .nav-resource-links { display: none; }
}
.landing-main { flex: 1; }

.hero-section { padding: 3rem 1.5rem; background: var(--home-hero-gradient); position: relative; overflow: hidden; }
.hero-section::before { content: ''; position: absolute; inset: 0; background: var(--home-hero-glow); pointer-events: none; }
.hero-container { max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 3rem; position: relative; z-index: 1; }
@media (min-width: 1024px) { .hero-container { grid-template-columns: 1fr 1fr; align-items: center; } }

.hero-eyebrow { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--home-accent); margin-bottom: 1rem; }
.hero-title { font-size: clamp(2rem, 8vw, 3.5rem); line-height: 1.1; color: var(--home-text-primary); margin-bottom: 1.5rem; letter-spacing: -0.02em; font-weight: 800; }
.hero-subtitle { font-size: 1.125rem; line-height: 1.7; color: var(--home-text-secondary); margin-bottom: 2rem; max-width: 500px; }
.hero-ctas { margin-top: 2.5rem; position: relative; z-index: 10; }
  .hero-actions { display: flex; align-items: center; gap: 1.25rem; flex-wrap: wrap; }
  
  :deep(.btn-hero-primary) { padding: 0.875rem 1.75rem; border-radius: 999px; font-weight: 600; font-size: 1.05rem; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); border: none; box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25); transition: transform 0.2s ease, box-shadow 0.2s ease; }
  :deep(.btn-hero-primary:hover) { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(37, 99, 235, 0.35); background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); }
  
  :deep(.btn-hero-secondary) { padding: 0.875rem 1.75rem; border-radius: 999px; font-weight: 600; font-size: 1.05rem; background: rgba(241, 245, 249, 0.8); border: 1px solid rgba(226, 232, 240, 0.8); color: #334155; transition: transform 0.2s ease, background 0.2s ease; }
  :deep(.btn-hero-secondary:hover) { transform: translateY(-2px); background: #f8fafc; color: #0f172a; border-color: #cbd5e1; }

  .social-proof { margin-top: 2.5rem; display: flex; flex-direction: column; gap: 0.75rem; }
  .github-badge { display: inline-flex; align-items: center; gap: 0.75rem; background: rgba(255, 255, 255, 0.6); border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 999px; padding: 0.35rem 1rem 0.35rem 0.35rem; text-decoration: none; width: fit-content; transition: all 0.2s ease; backdrop-filter: blur(8px); }
  .github-badge:hover { background: rgba(255, 255, 255, 0.9); box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05); transform: translateY(-2px); border-color: rgba(203, 213, 225, 0.8); }
  .github-icon { width: 2.25rem; height: 2.25rem; background: #0f172a; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; }
  .github-stats { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; font-weight: 600; color: var(--home-text-primary); }
  .star-count i { color: #eab308; margin-right: 0.2rem; }
  .fork-count i { margin-right: 0.2rem; }
  .separator { color: var(--home-text-secondary); opacity: 0.5; }
  .social-proof-text { font-size: 0.88rem; color: var(--home-text-secondary); margin: 0; margin-left: 0.5rem; font-weight: 500; }

  .loading-auth { display: flex; align-items: center; gap: 0.75rem; font-size: 1rem; color: var(--home-text-secondary); margin-top: 2rem; }

.hero-visual { position: relative; min-height: 400px; display: flex; align-items: center; justify-content: center; }
.visual-showcase { position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }
.visual-showcase::before { content: ''; position: absolute; width: 520px; height: 520px; border-radius: 50%; background: radial-gradient(circle, rgba(59, 130, 246, 0.08) 0%, rgba(59, 130, 246, 0) 68%); filter: blur(2px); }

.massive-logo { width: 160px; height: 160px; z-index: 5; filter: drop-shadow(0 15px 30px rgba(15, 118, 110, 0.2)); position: relative; }
@media (min-width: 768px) { .massive-logo { width: 200px; height: 200px; } }

.orbit-ring { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); border-radius: 50%; border: 1px solid rgba(37, 99, 235, 0.15); z-index: 1; animation: orbitPulse 8s ease-in-out infinite; }
.ring-1 { width: 280px; height: 280px; } 
.ring-2 { width: 440px; height: 440px; border: 1px solid rgba(37, 99, 235, 0.14); animation-delay: -1.5s; } 
.ring-3 { width: 620px; height: 620px; border: 1px dashed rgba(14, 165, 233, 0.2); animation-delay: -3s; }

.feature-chip { --chip-base-transform: translateY(0); position: absolute; transform: var(--chip-base-transform); display: flex; align-items: center; gap: 0.55rem; background: linear-gradient(145deg, rgba(255, 255, 255, 0.74), rgba(241, 248, 255, 0.78)); backdrop-filter: blur(8px); padding: 0.34rem 0.82rem 0.34rem 0.34rem; border-radius: 999px; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06); border: 1px solid rgba(173, 202, 255, 0.34); font-weight: 600; font-size: 0.78rem; color: var(--home-text-primary); z-index: 10; white-space: nowrap; transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease; animation: orbitFloat 6s ease-in-out infinite; }
.feature-chip:hover { transform: var(--chip-base-transform) scale(1.02); box-shadow: 0 8px 18px rgba(30, 64, 175, 0.1); border-color: rgba(96, 165, 250, 0.42); animation-play-state: paused; z-index: 20; }
.chip-icon { width: 2rem; height: 2rem; border-radius: 50%; background: rgba(15, 118, 110, 0.1); color: var(--home-accent); display: flex; align-items: center; justify-content: center; }
.chip-2 .chip-icon { background: rgba(37,99,235,0.1); color: #2563eb; } 
.chip-4 .chip-icon { background: rgba(147,51,234,0.1); color: #9333ea; } 
.chip-5 .chip-icon { background: rgba(234,88,12,0.1); color: #ea580c; } 
.chip-6 .chip-icon { background: rgba(225,29,72,0.1); color: #e11d48; }
.chip-7 .chip-icon { background: rgba(79,70,229,0.1); color: #4f46e5; }

.chip-1 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% + 90px), calc(-50% - 107px)); animation-delay: 0s; animation-duration: 7s; } 
.chip-2 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% + 135px), calc(-50% - 173px)); animation-delay: -1.5s; animation-duration: 8.5s; }
.chip-3 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% + 195px), calc(-50% + 102px)); animation-delay: -3s; animation-duration: 6.5s; }
.chip-4 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% - 99px), calc(-50% + 99px)); animation-delay: -2s; animation-duration: 7.5s; }
.chip-5 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% - 80px), calc(-50% + 205px)); animation-delay: -4.5s; animation-duration: 8s;}
.chip-6 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% - 155px), calc(-50% - 155px)); animation-delay: -0.5s; animation-duration: 9s; }
.chip-7 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% - 232px), calc(-50% + 8px)); animation-delay: -5.2s; animation-duration: 8.2s; }

@media (min-width: 1024px) {
  .hero-visual { min-height: 550px; }
  .visual-showcase { transform: translateX(-84px); }
}
@media (max-width: 1023px) {
  .hero-visual { min-height: 450px; margin-top: 2rem; margin-bottom: 1rem; } 
  .visual-showcase { transform: scale(0.85); transform-origin: center; }
  .massive-logo { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
}
@media (max-width: 767px) {
    .hero-container { gap: 1.5rem; text-align: center; }
    .hero-content { display: flex; flex-direction: column; align-items: center; }
    .hero-visual.mobile-orbit {
      min-height: 360px;
      width: 100%;
      margin: 0.2rem 0 1rem;
      overflow: visible;
    }
    .hero-visual.mobile-orbit .visual-showcase {
      transform: scale(0.64);
      transform-origin: center;
    }
    .hero-visual.mobile-orbit .massive-logo {
      width: 190px;
      height: 190px;
      opacity: 1;
      z-index: 16;
      filter: drop-shadow(0 16px 34px rgba(37, 99, 235, 0.28));
    }
  .hero-visual.mobile-orbit .ring-3 { display: none; }
    .hero-actions { justify-content: center; width: 100%; flex-direction: column; gap: 1rem; }
    .btn-hero-primary, .btn-hero-secondary { width: 100%; justify-content: center; }
    .social-proof { align-items: center; margin-bottom: 1.1rem; }
    .social-proof-text { text-align: center; margin-left: 0; }
    
.hero-visual { display: flex; min-height: 380px; margin-top: 1rem; margin-bottom: 0; overflow: visible; align-items: center; justify-content: center; }
    .visual-showcase { transform: scale(0.6); transform-origin: center; width: 100%; height: 100%; }
    .visual-showcase::before { width: 400px; height: 400px; filter: blur(15px); background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, rgba(59, 130, 246, 0) 70%); }
    .massive-logo { width: 160px; height: 160px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
    
  .feature-panel-wrapper { margin-top: 0.35rem; padding-top: 0; }
  .deployment-panel-body { padding: 0.95rem; }
  .deployment-chip-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }

.quick-stats-section { padding: 3rem 0; background: var(--home-bg); }
.content-wrapper { max-width: 1400px; margin: 0 auto; padding: 0 1.5rem; }
.quick-stats-grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }
@media (min-width: 768px) { .quick-stats-grid { grid-template-columns: repeat(3, 1fr); } }

.quick-stat-tile { background: var(--home-card-bg); border: 1px solid var(--home-border); border-radius: 1rem; padding: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem; box-shadow: var(--home-shadow); }
.quick-stat-head { display: flex; align-items: center; gap: 0.75rem; }
.quick-stat-icon { width: 2.5rem; height: 2.5rem; border-radius: 0.5rem; background: rgba(15, 118, 110, 0.1); color: var(--home-accent); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
.quick-stat-latest .quick-stat-icon { background: rgba(14, 165, 233, 0.1); color: #0ea5e9; }
.quick-stat-distance .quick-stat-icon { background: rgba(37, 99, 235, 0.1); color: #2563eb; }
.quick-stat-label { margin: 0; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--home-text-secondary); }
.quick-stat-value { margin: 0; font-size: 1.5rem; font-weight: 700; color: var(--home-text-primary); }

.feature-panel-wrapper { width: 100%; max-width: 1400px; margin: -1.15rem auto 0; padding: 0; position: relative; z-index: 10; display: grid; grid-template-columns: minmax(320px, 0.38fr) minmax(0, 0.62fr); gap: 1rem; align-items: stretch; }
.deployment-panel,
.feature-panel { width: 100%; background: rgba(255, 255, 255, 0.8); border: 1px solid rgba(203, 213, 225, 0.6); border-radius: 1rem; box-shadow: 0 8px 18px rgba(15, 23, 42, 0.06); overflow: hidden; }

.feature-panel {
  --feature-accent: #2563eb;
  --feature-accent-soft: rgba(37, 99, 235, 0.11);
  --feature-accent-shadow: rgba(37, 99, 235, 0.26);
}
.feature-panel.chip-1-color { --feature-accent: #0ea5e9; --feature-accent-soft: rgba(14, 165, 233, 0.13); --feature-accent-shadow: rgba(14, 165, 233, 0.3); }
.feature-panel.chip-2-color { --feature-accent: #2563eb; --feature-accent-soft: rgba(37, 99, 235, 0.12); --feature-accent-shadow: rgba(37, 99, 235, 0.28); }
.feature-panel.chip-3-color { --feature-accent: #0f766e; --feature-accent-soft: rgba(15, 118, 110, 0.12); --feature-accent-shadow: rgba(15, 118, 110, 0.28); }
.feature-panel.chip-4-color { --feature-accent: #9333ea; --feature-accent-soft: rgba(147, 51, 234, 0.13); --feature-accent-shadow: rgba(147, 51, 234, 0.28); }
.feature-panel.chip-5-color { --feature-accent: #ea580c; --feature-accent-soft: rgba(234, 88, 12, 0.13); --feature-accent-shadow: rgba(234, 88, 12, 0.28); }
.feature-panel.chip-6-color { --feature-accent: #e11d48; --feature-accent-soft: rgba(225, 29, 72, 0.13); --feature-accent-shadow: rgba(225, 29, 72, 0.28); }
.feature-panel.chip-7-color { --feature-accent: #4f46e5; --feature-accent-soft: rgba(79, 70, 229, 0.13); --feature-accent-shadow: rgba(79, 70, 229, 0.28); }

.deployment-panel { display: flex; flex-direction: column; }
.deployment-panel-header,
.feature-panel-header { padding: 0.92rem 1.1rem 0.72rem; border-bottom: 1px solid rgba(203, 213, 225, 0.55); background: rgba(248, 250, 252, 0.56); }
.deployment-title { margin: 0; font-size: 1.12rem; line-height: 1.3; color: var(--home-text-primary); font-weight: 700; }
.deployment-panel-body { padding: 1rem 1.1rem; display: flex; flex-direction: column; gap: 0.85rem; }
.deployment-summary { margin: 0; font-size: 0.9rem; line-height: 1.52; color: var(--home-text-secondary); }
.deployment-chip-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.45rem; }
.deployment-chip { display: inline-flex; align-items: center; gap: 0.4rem; border-radius: 0.72rem; padding: 0.45rem 0.55rem; border: 1px solid rgba(203, 213, 225, 0.76); background: rgba(248, 250, 252, 0.62); color: #334155; font-size: 0.8rem; font-weight: 600; white-space: nowrap; }
.deployment-chip i { font-size: 0.82rem; opacity: 0.9; }

.deployment-points { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 0.45rem; }
.deployment-points li { display: flex; align-items: flex-start; gap: 0.45rem; font-size: 0.84rem; line-height: 1.45; color: var(--home-text-secondary); }
.deployment-points i { font-size: 0.86rem; color: #2563eb; margin-top: 0.1rem; }

.feature-panel-kicker { margin: 0 0 0.75rem; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: var(--home-text-secondary); }
.mobile-panel-header { padding: 0.65rem 0.95rem 0.65rem; }
.mobile-panel-tab-switch { display: none; }
.feature-panel-header-inner { border-top: 1px solid rgba(203, 213, 225, 0.52); }
.mobile-deployment-body { border-top: 1px solid rgba(203, 213, 225, 0.52); }
.feature-tabs { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.feature-tab { border: 1px solid rgba(203, 213, 225, 0.9); background: rgba(255, 255, 255, 0.9); color: #334155; border-radius: 0.75rem; height: 2.5rem; padding: 0 0.8rem; display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.84rem; font-weight: 600; cursor: pointer; transition: all 0.25s ease; }
.feature-tab i { font-size: 0.92rem; color: #64748b; }
.feature-tab:hover { border-color: rgba(96, 165, 250, 0.7); color: #1e293b; }
.feature-tab.active { background: var(--feature-accent); border-color: var(--feature-accent); color: #ffffff; box-shadow: 0 8px 18px var(--feature-accent-shadow); }
.feature-tab.active i { color: #dbeafe; }

.feature-panel-body { display: block; padding: 1.15rem 1.25rem 1.2rem; min-height: 214px; }
.feature-panel-copy { display: flex; flex-direction: column; justify-content: center; }
.feature-panel-copy h3 { margin: 0 0 0.5rem; font-size: 1.3rem; font-weight: 700; color: var(--home-text-primary); }
.feature-panel-copy p { margin: 0; font-size: 0.98rem; line-height: 1.62; color: var(--home-text-secondary); max-width: 74ch; min-height: calc(1.62em * 2); }
.feature-highlight-list { margin: 0.95rem 0 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.6rem 0.8rem; }
.feature-highlight-list li { display: flex; align-items: flex-start; gap: 0.45rem; color: var(--home-text-secondary); font-size: 0.88rem; line-height: 1.45; border: 1px solid rgba(203, 213, 225, 0.62); border-left: 3px solid var(--feature-accent); background: linear-gradient(90deg, var(--feature-accent-soft), rgba(255, 255, 255, 0.2)); border-radius: 0.65rem; padding: 0.48rem 0.58rem; }
.feature-highlight-list i { font-size: 0.9rem; color: var(--feature-accent); margin-top: 0.08rem; }

@media (max-width: 1023px) {
  .feature-panel-wrapper {
    grid-template-columns: 1fr;
    max-width: 100%;
    margin-top: 0.2rem;
    gap: 0.85rem;
  }
  .feature-panel,
  .deployment-panel {
    width: 100%;
    max-width: 100%;
  }
  .feature-panel { order: 1; }
  .deployment-panel { order: 2; }
  .feature-panel { max-width: 100%; }
  .feature-tab { height: 2.35rem; padding: 0 0.7rem; font-size: 0.8rem; }
}

@media (max-width: 767px) {
  .feature-panel-wrapper {
    margin-top: 0.35rem;
    padding-top: 0;
    gap: 0.75rem;
  }
  .mobile-panel-tab-switch {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0;
    background: rgba(226, 232, 240, 0.48);
    border: 1px solid rgba(203, 213, 225, 0.7);
    border-radius: 0.85rem;
    padding: 0.35rem;
    margin-bottom: 0.5rem;
  }
  .mobile-panel-tab {
    border: 1px solid transparent;
    background: transparent;
    color: #334155;
    border-radius: 0.65rem;
    height: 2.65rem;
    padding: 0.5rem 0.75rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    font-size: 0.86rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  }
  .mobile-panel-tab:hover:not(.active) {
    background: rgba(255, 255, 255, 0.55);
  }
  .mobile-panel-tab.active {
    background: #ffffff;
    border-color: transparent;
    color: #1e40af;
    box-shadow: 0 2px 8px rgba(30, 64, 175, 0.15);
  }
  .mobile-panel-tab.active i { color: #1e40af; }
  .deployment-panel-body { padding: 0.95rem; }
  .deployment-chip-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .deployment-chip {
    white-space: normal;
    text-align: left;
    min-height: 2.2rem;
  }
  .feature-panel-header { padding: 0.95rem 0.95rem 0.75rem; }
  .feature-tabs { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.45rem; }
  .feature-tab { justify-content: center; }
  .feature-panel-body { padding: 0.95rem; min-height: auto; }
  .feature-panel-copy p { font-size: 0.95rem; }
  .feature-highlight-list { grid-template-columns: 1fr; gap: 0.5rem; margin-top: 0.8rem; }
}

  .fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
  .fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(10px); }

  .landing-footer { padding: 2rem 0; border-top: 1px solid var(--home-border); text-align: center; color: var(--home-text-secondary); font-size: 0.9rem; }

  @keyframes orbitPulse {
    0%,
    100% { opacity: 0.78; }
  50% { opacity: 1; }
}

@keyframes orbitFloat {
  0%, 100% { margin-top: 0px; }
  50% { margin-top: -12px; }
}

.p-dark .landing-page {
  --home-bg: #020617;
  --home-card-bg: #0f172a;
  --home-border: #1e293b;
  --home-text-primary: #f8fafc;
  --home-text-secondary: #94a3b8;
  --home-shadow: 0 12px 30px rgba(0, 0, 0, 0.45);
  --home-hero-gradient: linear-gradient(160deg, #020617 0%, #0a1128 50%, #03081a 100%);
  --home-hero-glow: radial-gradient(ellipse at 80% 20%, rgba(59, 130, 246, 0.15) 0%, transparent 60%);
  background: radial-gradient(circle at 8% 10%, rgba(37, 99, 235, 0.05) 0%, rgba(37, 99, 235, 0) 34%), radial-gradient(circle at 90% 75%, rgba(14, 165, 233, 0.05) 0%, rgba(14, 165, 233, 0) 30%), var(--home-bg);
}
.p-dark .landing-header { background: rgba(2, 6, 23, 0.85); border-bottom-color: rgba(255,255,255,0.05); }
.p-dark .theme-button :deep(.p-button) {
  background: rgba(15, 23, 42, 0.9);
  border-color: rgba(148, 163, 184, 0.55);
  color: #e2e8f0;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.24);
}
.p-dark .theme-button :deep(.p-button:hover) {
  background: rgba(30, 41, 59, 0.95);
  border-color: rgba(203, 213, 225, 0.72);
  color: #f8fafc;
}
.p-dark .nav-link-pill { background: rgba(15, 23, 42, 0.7); border-color: rgba(148, 163, 184, 0.35); color: #cbd5e1; }
.p-dark .nav-link-pill:hover { background: rgba(30, 41, 59, 0.82); border-color: rgba(148, 163, 184, 0.55); color: #e2e8f0; }
.p-dark .nav-version-badge { background: rgba(255, 255, 255, 0.92); border-color: rgba(255, 255, 255, 0.45); color: #6d28d9; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2); }
.p-dark .feature-chip { background: rgba(15, 23, 42, 0.62); border-color: rgba(100, 116, 139, 0.62); box-shadow: 0 4px 10px rgba(0, 0, 0, 0.18); }
.p-dark .feature-chip:hover, .p-dark .feature-chip.active { border-color: rgba(59, 130, 246, 0.5); box-shadow: 0 8px 16px rgba(37, 99, 235, 0.2); background: rgba(30, 41, 59, 0.74); }
.p-dark .quick-stat-tile, .p-dark .welcome-back-box { background: rgba(15, 23, 42, 0.6); border-color: rgba(255,255,255,0.08); }
.p-dark .welcome-back-box { background: rgba(30, 41, 59, 0.5); }
.p-dark .orbit-ring { border-color: rgba(255,255,255,0.05); }

.p-dark .github-badge { background: rgba(30, 41, 59, 0.4); border-color: rgba(255, 255, 255, 0.08); }
.p-dark .github-badge:hover { background: rgba(30, 41, 59, 0.8); border-color: rgba(255, 255, 255, 0.15); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); }
.p-dark .github-icon { background: white; color: #0f172a; }

.p-dark .deployment-panel,
.p-dark .feature-panel { background: linear-gradient(145deg, rgba(15, 23, 42, 0.78), rgba(15, 23, 42, 0.68)); border-color: rgba(148, 163, 184, 0.26); box-shadow: 0 10px 22px rgba(0, 0, 0, 0.24); }

.p-dark .deployment-panel-header,
.p-dark .feature-panel-header { border-bottom-color: rgba(148, 163, 184, 0.2); background: rgba(30, 41, 59, 0.5); }

.p-dark .deployment-chip { background: rgba(15, 23, 42, 0.52); border-color: rgba(148, 163, 184, 0.42); color: #cbd5e1; }
.p-dark .deployment-chip i { color: #94a3b8; }

.p-dark .deployment-points li { color: #94a3b8; }
.p-dark .deployment-points i { color: #60a5fa; }

.p-dark .feature-tab { background: rgba(15, 23, 42, 0.85); border-color: rgba(148, 163, 184, 0.4); color: #cbd5e1; }
.p-dark .feature-tab i { color: #94a3b8; }
.p-dark .feature-tab:hover { border-color: rgba(96, 165, 250, 0.6); color: #e2e8f0; }
.p-dark .feature-tab.active { background: var(--feature-accent); border-color: var(--feature-accent); color: #ffffff; box-shadow: 0 8px 18px var(--feature-accent-shadow); }
.p-dark .feature-tab.active i { color: #dbeafe; }
.p-dark .feature-panel-header-inner,
.p-dark .mobile-deployment-body { border-top-color: rgba(148, 163, 184, 0.2); }
.p-dark .mobile-panel-tab-switch {
  background: rgba(30, 41, 59, 0.6);
  border-color: rgba(148, 163, 184, 0.25);
}
.p-dark .mobile-panel-tab {
  background: transparent;
  border-color: transparent;
  color: #cbd5e1;
}
.p-dark .mobile-panel-tab:hover:not(.active) {
  background: rgba(71, 85, 105, 0.35);
}
.p-dark .mobile-panel-tab.active {
  background: #1e293b;
  border-color: transparent;
  color: #60a5fa;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}
.p-dark .mobile-panel-tab.active i {
  color: #60a5fa;
}
.p-dark .feature-highlight-list li { color: #94a3b8; border-color: rgba(148, 163, 184, 0.32); background: linear-gradient(90deg, var(--feature-accent-soft), rgba(15, 23, 42, 0.14)); }
.p-dark .feature-highlight-list i { color: var(--feature-accent); }
</style>
