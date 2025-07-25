<template>
  <canvas ref="canvas" class="starfield-canvas"></canvas>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as THREE from 'three';

export default {
  name: 'Starfield',
  setup() {
    const canvas = ref(null);
    let scene, camera, renderer, stars, animationId;
    let rotationSpeedY = 0.001;
    let rotationSpeedX = 0.0005;
    let scrollSpeed = 0;
    let mouseX = 0;
    let mouseY = 0;

    onMounted(() => {
      scene = new THREE.Scene();
      camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      renderer = new THREE.WebGLRenderer({ canvas: canvas.value, alpha: false });
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setClearColor(0x000000, 1); // black background

      const starsGeometry = new THREE.BufferGeometry();
      const starCount = 1000;
      const positionArray = new Float32Array(starCount * 3);

      for (let i = 0; i < starCount * 3; i++) {
        positionArray[i] = (Math.random() - 0.5) * 2000;
      }

      starsGeometry.setAttribute('position', new THREE.BufferAttribute(positionArray, 3));
      const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 2 });
      stars = new THREE.Points(starsGeometry, starsMaterial);

      scene.add(stars);
      camera.position.z = 5;

      const animate = () => {
        animationId = requestAnimationFrame(animate);
        // Rotate stars with base speed plus scroll speed
        stars.rotation.y += rotationSpeedY + scrollSpeed * 0.0005;
        stars.rotation.x += rotationSpeedX + scrollSpeed * 0.0003;

        // Mouse interaction: rotate stars based on mouse position
        stars.rotation.y += (mouseX / window.innerWidth - 0.5) * 0.01;
        stars.rotation.x += (mouseY / window.innerHeight - 0.5) * 0.01;

        renderer.render(scene, camera);
      };

      animate();

      const handleResize = () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
      };

      const handleMouseMove = (event) => {
        mouseX = event.clientX;
        mouseY = event.clientY;
      };

      window.addEventListener('resize', handleResize);
      window.addEventListener('mousemove', handleMouseMove);

      onBeforeUnmount(() => {
        window.removeEventListener('resize', handleResize);
        window.removeEventListener('scroll', handleScroll);
        window.removeEventListener('mousemove', handleMouseMove);
        cancelAnimationFrame(animationId);
        renderer.dispose();
      });
    });

    return {
      canvas,
    };
  },
};
</script>

<style scoped>
.starfield-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
  display: block;
}
</style>
