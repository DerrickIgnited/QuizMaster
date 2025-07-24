<template>
  <Particles
    id="tsparticles"
    :options="{
      fpsLimit: 60,
      background: { color: '#000000' },
      particles: {
        number: {
          value: 120,
          density: { enable: true, area: 800 }
        },
        color: { value: '#ffffff' },
        shape: { type: 'circle' },
        opacity: {
          value: 0.8,
          random: { enable: true, minimumValue: 0.3 }
        },
        size: {
          value: 1.5,
          random: { enable: true, minimumValue: 0.5 }
        },
        move: {
          enable: true,
          speed: 0.2,
          direction: 'none',
          outModes: { default: 'out' }
        }
      },
      interactivity: {
        events: {
          onHover: { enable: false },
          onClick: { enable: false }
        }
      },
      detectRetina: true
    }"
    class="starfield"
  />
</template>

<style scoped>
.starfield {
  position: fixed;
  inset: 0;
  z-index: -1;
}
</style>
