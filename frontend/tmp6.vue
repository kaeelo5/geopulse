<template>
  <div class="landing-page">
    <header class="landing-header">
      <div class="nav-container">
        <div class="logo-container">
          <img src="/geopulse-logo.svg" alt="GeoPulse" class="nav-logo" />
          <span class="logo-text">GeoPulse</span>
        </div>
        <div class="nav-actions">
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
            
            <div class="hero-ctas" v-if="!isResolvingAuth">
              <template v-if="!authStore.isAuthenticated">
                  <div class="hero-actions">
                    <Button label="Start Your Journey" icon="pi pi-arrow-right" iconPos="right" as="router-link" to="/register" size="large" class="btn-hero-primary" />
                    <Button label="Sign In" as="router-link" to="/login" size="large" class="btn-hero-secondary" />
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

          <div class="hero-visual">
            <div class="visual-showcase">
              <div class="orbit-ring ring-1"></div>
              <div class="orbit-ring ring-2"></div>
              <div class="orbit-ring ring-3"></div>
              <img src="/geopulse-logo.svg" alt="GeoPulse logo" class="massive-logo" />
              <div class="feature-chip chip-1"><div class="chip-icon"><i class="pi pi-send"></i></div><span>Live Tracking</span><div class="chip-tooltip">Stream GPS points as they arrive and watch your movement unfold live.</div></div>
              <div class="feature-chip chip-2"><div class="chip-icon"><i class="pi pi-download"></i></div><span>Smart Import</span><div class="chip-tooltip">Effortlessly import bulk GPS history from external sources like Google Takeout.</div></div>
              <div class="feature-chip chip-3"><div class="chip-icon"><i class="pi pi-calendar"></i></div><span>Auto-Timeline</span><div class="chip-tooltip">Watch your raw GPS points automatically organize into distinct trips and stops.</div></div>
              <div class="feature-chip chip-4"><div class="chip-icon"><i class="pi pi-chart-line"></i></div><span>Deep Insights</span><div class="chip-tooltip">Analyze your travel patterns with built-in insights and rich visualizations.</div></div>
              <div class="feature-chip chip-5"><div class="chip-icon"><i class="pi pi-images"></i></div><span>Immich Integration</span><div class="chip-tooltip">Connect Immich to seamlessly plot your photos along your journey timeline.</div></div>
              <div class="feature-chip chip-6"><div class="chip-icon"><i class="pi pi-shield"></i></div><span>SSO and Roles</span><div class="chip-tooltip">Enforce secure multi-user access with built-in Single Sign-On and permissions.</div></div>
            </div>
          </div>
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

      <section v-if="!isResolvingAuth && !authStore.isAuthenticated" class="features-section">
        <div class="content-wrapper">
          <div class="section-header">
            <h2>Core Capabilities</h2>
            <p>Built for self-hosted tracking: ingest data, analyze movement, and control your sharing entirely.</p>
          </div>
          <div class="feature-bento-grid">
            <Card v-for="feature in visibleFeatures" :key="feature.id" class="bento-card">
              <template #content>
                <div class="bento-icon"><i :class="feature.icon"></i></div>
                <h3>{{ feature.title }}</h3>
                <p>{{ feature.description }}</p>
              </template>
            </Card>
          </div>
          <Button v-if="!isDesktopViewport && hasHiddenFeatures" :label="showAllFeatures ? 'Show fewer' : 'Show all capabilities'" :icon="showAllFeatures ? 'pi pi-angle-up' : 'pi pi-angle-down'" severity="secondary" outlined class="mobile-feature-toggle" @click="toggleFeatureVisibility" />
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
import Card from 'primevue/card'

const router = useRouter()
const authStore = useAuthStore()

const isResolvingAuth = ref(true)
const isLoginAvailable = ref(false)
const isRegistrationAvailable = ref(false)
const isMobileViewport = ref(false)
const isDesktopViewport = ref(true)
const showAllFeatures = ref(false)
const continueDestination = ref({ path: '/app/timeline' })
const latestGpsUpdateLabel = ref('')
const distanceTodayLabel = ref('')
const timeMovingTodayLabel = ref('')

const features = [
  { id: 1, title: 'Live Tracking', description: 'Stream GPS points as they arrive and watch your movement unfold live.', icon: 'pi pi-send', colorClass: 'chip-1-color' },
  { id: 2, title: 'Smart Import', description: 'Effortlessly import bulk GPS history from external sources like Google Takeout.', icon: 'pi pi-download', colorClass: 'chip-2-color' },
  { id: 3, title: 'Auto-Timeline', description: 'Watch your raw GPS points automatically organize into distinct trips and stops.', icon: 'pi pi-calendar', colorClass: 'chip-3-color' },
  { id: 4, title: 'Deep Insights', description: 'Analyze your travel patterns with built-in insights and rich visualizations.', icon: 'pi pi-chart-line', colorClass: 'chip-4-color' },
  { id: 5, title: 'Immich Integration', description: 'Connect Immich to seamlessly plot your photos along your journey timeline.', icon: 'pi pi-images', colorClass: 'chip-5-color' },
  { id: 6, title: 'SSO and Roles', description: 'Enforce secure multi-user access with built-in Single Sign-On and permissions.', icon: 'pi pi-shield', colorClass: 'chip-6-color' }
]

const heroTitle = computed(() => {
  return authStore.isAuthenticated ? 'Welcome back' : 'Your location, your data'
})

const shouldShowQuickStats = computed(() => {
  return authStore.isAuthenticated && !isResolvingAuth.value
})

const visibleFeatures = computed(() => {
  if (isDesktopViewport.value) return features
  if (showAllFeatures.value) return features
  return features.slice(0, 3)
})

const hasHiddenFeatures = computed(() => {
  return features.length > 3 && !isDesktopViewport.value
})

const handleSignOut = async () => {
  await authStore.logout()
  router.push('/')
}

const toggleFeatureVisibility = () => {
  showAllFeatures.value = !showAllFeatures.value
}

const updateViewportState = () => {
  isMobileViewport.value = window.innerWidth < 768
  isDesktopViewport.value = window.innerWidth >= 1024
}

const updateUserStats = () => {
  latestGpsUpdateLabel.value = '2 minutes ago'
  distanceTodayLabel.value = '12.4 km'
  timeMovingTodayLabel.value = '45 min'
}

onMounted(async () => {
  updateViewportState()
  window.addEventListener('resize', updateViewportState)
  
  try {
    await authStore.resolveAuthentication()
    isLoginAvailable.value = authStore.loginAvailable
    isRegistrationAvailable.value = authStore.registrationAvailable
  } finally {
    isResolvingAuth.value = false
  }
  
  if (authStore.isAuthenticated) {
    updateUserStats()
  }
})

onBeforeUnmount(() => {
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
html, body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; }

.landing-page { position: relative; background: radial-gradient(circle at 8% 10%, #dbeafe 0%, rgba(219, 234, 254, 0) 34%), radial-gradient(circle at 90% 75%, #dcfce7 0%, rgba(220, 252, 231, 0) 30%), var(--home-bg); min-height: 100vh; display: flex; flex-direction: column; }
.landing-header { background: rgba(244, 248, 255, 0.78); border-bottom: 1px solid var(--home-border); padding: 0.75rem 0; position: sticky; top: 0; z-index: 100; backdrop-filter: blur(10px); }
.nav-container { max-width: 1400px; margin: 0 auto; padding: 0 1.5rem; display: flex; justify-content: space-between; align-items: center; }
.logo-container { display: flex; align-items: center; gap: 0.75rem; }
.nav-logo { height: 32px; width: auto; }
.logo-text { font-size: 1.1rem; font-weight: 700; color: var(--home-text-primary); letter-spacing: -0.02em; }
.nav-actions { display: flex; align-items: center; gap: 1rem; }
.auth-actions { display: flex; align-items: center; gap: 0.5rem; }
.landing-main { flex: 1; }

.hero-section { padding: 3rem 1.5rem; background: var(--home-hero-gradient); position: relative; overflow: hidden; border-bottom: 1px solid rgba(15, 23, 42, 0.04); }
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

.feature-chip { --chip-base-transform: translateY(0); position: absolute; transform: var(--chip-base-transform); display: flex; align-items: center; gap: 0.6rem; background: linear-gradient(145deg, rgba(255, 255, 255, 0.9), rgba(241, 248, 255, 0.92)); backdrop-filter: blur(12px); padding: 0.4rem 1rem 0.4rem 0.4rem; border-radius: 999px; box-shadow: 0 6px 18px rgba(15, 23, 42, 0.1); border: 1px solid rgba(173, 202, 255, 0.45); font-weight: 600; font-size: 0.85rem; color: var(--home-text-primary); z-index: 10; white-space: nowrap; transition: transform 0.3s ease, box-shadow 0.3s ease; animation: orbitFloat 6s ease-in-out infinite; }
.feature-chip:hover { transform: var(--chip-base-transform) scale(1.05); box-shadow: 0 10px 24px rgba(30, 64, 175, 0.16); animation-play-state: paused; z-index: 20; }
.chip-icon { width: 2rem; height: 2rem; border-radius: 50%; background: rgba(15, 118, 110, 0.1); color: var(--home-accent); display: flex; align-items: center; justify-content: center; }
.chip-2 .chip-icon { background: rgba(37,99,235,0.1); color: #2563eb; } 
.chip-4 .chip-icon { background: rgba(147,51,234,0.1); color: #9333ea; } 
.chip-5 .chip-icon { background: rgba(234,88,12,0.1); color: #ea580c; } 
.chip-6 .chip-icon { background: rgba(225,29,72,0.1); color: #e11d48; }

  .chip-tooltip { position: absolute; top: calc(100% + 15px); left: 50%; transform: translateX(-50%) translateY(10px) scale(0.95); width: 300px; padding: 1.25rem 1.5rem; background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.98)); backdrop-filter: blur(20px); border: 1px solid rgba(226, 232, 240, 0.8); border-radius: 1.25rem; box-shadow: 0 20px 40px rgba(15, 23, 42, 0.15), 0 4px 6px rgba(15, 23, 42, 0.05); color: var(--home-text-secondary); font-size: 0.95rem; font-weight: 400; line-height: 1.6; white-space: normal; text-align: center; opacity: 0; visibility: hidden; pointer-events: none; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); z-index: 100; }
  .chip-3 .chip-tooltip, .chip-5 .chip-tooltip, .chip-6 .chip-tooltip { top: auto; bottom: calc(100% + 15px); transform: translateX(-50%) translateY(-10px) scale(0.95); }
  .feature-chip:hover .chip-tooltip { opacity: 1; visibility: visible; transform: translateX(-50%) translateY(0) scale(1); }

@media (min-width: 1024px) {
  .chip-1 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% + 90px), calc(-50% - 107px)); animation-delay: 0s; animation-duration: 7s; } 
    .chip-2 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% + 135px), calc(-50% - 173px)); animation-delay: -1.5s; animation-duration: 8.5s; }
    .chip-3 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% + 195px), calc(-50% + 102px)); animation-delay: -3s; animation-duration: 6.5s; }
  .chip-4 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% - 99px), calc(-50% + 99px)); animation-delay: -2s; animation-duration: 7.5s; }
    .chip-5 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% - 80px), calc(-50% + 205px)); animation-delay: -4.5s; animation-duration: 8s;}
  .chip-6 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% - 155px), calc(-50% - 155px)); animation-delay: -0.5s; animation-duration: 9s; }
}
@media (max-width: 1023px) {
  .hero-visual { min-height: 400px; overflow: hidden; padding-bottom: 2rem; } 
  .massive-logo { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
  .chip-1 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% + 76px), calc(-50% - 91px)); animation-delay: 0s; animation-duration: 7s; }
    .chip-2 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% + 114px), calc(-50% - 147px)); animation-delay: -1.5s; animation-duration: 8.5s; }
    .chip-3 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% + 165px), calc(-50% + 86px)); animation-delay: -3s; animation-duration: 6.5s; }
  .chip-4 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% - 84px), calc(-50% + 84px)); animation-delay: -2s; animation-duration: 7.5s; }
    .chip-5 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% - 68px), calc(-50% + 173px)); animation-delay: -4.5s; animation-duration: 8s;}
  .chip-6 { top: 50%; left: 50%; --chip-base-transform: translate(calc(-50% - 131px), calc(-50% - 131px)); animation-delay: -0.5s; animation-duration: 9s; }
  .orbit-ring { transform: translate(-50%, -50%) scale(0.85); }
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

.features-section { padding: 5rem 0; background: var(--home-bg); }
.section-header { text-align: center; margin-bottom: 4rem; max-width: 700px; margin-left: auto; margin-right: auto; }
.section-header h2 { font-size: clamp(2rem, 4vw, 2.5rem); margin: 0 0 1rem 0; letter-spacing: -0.02em; color: var(--home-text-primary); }
.section-header p { font-size: 1.1rem; color: var(--home-text-secondary); margin: 0; line-height: 1.6; }

.feature-bento-grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
@media (min-width: 768px) { .feature-bento-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .feature-bento-grid { grid-template-columns: repeat(3, 1fr); } }

.bento-card { background: linear-gradient(170deg, rgba(255, 255, 255, 0.96), rgba(243, 249, 255, 0.9)); border: 1px solid var(--home-border); border-radius: 1.25rem; box-shadow: var(--home-shadow); transition: transform 0.2s ease, box-shadow 0.2s ease; height: 100%; }
.bento-card:hover { transform: translateY(-4px); box-shadow: 0 15px 34px rgba(23, 37, 84, 0.12); }
.bento-card :deep(.p-card-body) { padding: 2rem; height: 100%; display: flex; flex-direction: column; }
.bento-card :deep(.p-card-content) { padding: 0; flex: 1; display: flex; flex-direction: column; }

.bento-icon { width: 3rem; height: 3rem; border-radius: 0.75rem; background: linear-gradient(135deg, rgba(15, 118, 110, 0.15) 0%, rgba(14, 165, 233, 0.1) 100%); color: var(--home-accent); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; margin-bottom: 1.5rem; border: 1px solid rgba(15, 118, 110, 0.2); }
.bento-card h3 { margin: 0 0 0.75rem 0; font-size: 1.2rem; font-weight: 700; color: var(--home-text-primary); }
.bento-card p { margin: 0; font-size: 0.95rem; line-height: 1.6; color: var(--home-text-secondary); flex: 1; }

.mobile-feature-toggle { margin-top: 2rem; width: 100%; }
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
}
.p-dark .landing-header { background: rgba(2, 6, 23, 0.85); border-bottom-color: rgba(255,255,255,0.05); }
.p-dark .feature-chip { background: rgba(15, 23, 42, 0.85); border-color: #334155; }
.p-dark .bento-card, .p-dark .quick-stat-tile, .p-dark .welcome-back-box { background: rgba(15, 23, 42, 0.6); border-color: rgba(255,255,255,0.08); }
.p-dark .welcome-back-box { background: rgba(30, 41, 59, 0.5); }
.p-dark .orbit-ring { border-color: rgba(255,255,255,0.05); }
</style>
