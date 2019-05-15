<template>
  <div class="simple-desktop">
    <div class="cover">
      <img src="https://source.unsplash.com/collection/2402988/1000x1000" alt="Nature picture">
      <div class="overlay">
        <i id="options" class="fas fa-cog fa-2x"></i>
      </div>
    </div>

    <div class="footer">
      <h4 id="name">{{ desktop.getName() }}</h4>
      <p>{{ desktop.getDescription() }}&nbsp;</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'simple-desktop',
  props: ['desktop']
}
</script>

<style lang="scss" scoped>
.simple-desktop {
  // Visual
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
  overflow: hidden;

  // Position
  display: flex;
  flex-flow: column nowrap;

  .cover {
    // Position
    position: relative;

    &:hover {
      .overlay {
        // Visual
        opacity: 100;
      }
    }

    img {
      // Size
      width: 100%;
    }

    .overlay {
      // Size
      width: 100%;
      height: 100%;

      // Position
      position: absolute;
      top: 0px;
      left: 0px;

      // Visual
      opacity: 0;
      background: #00000077;
      transition: 0.25s ease-in-out;

      #options {
        // Position
        position: absolute;
        top: 10px;
        right: 10px;

        // Visual
        color: #ffffff;
        text-shadow: 0 3px 6px rgba(0, 0, 0, 0.16),
          0 3px 6px rgba(0, 0, 0, 0.23);
        cursor: pointer;
        transition: transform 0.25s ease-in-out;

        &:hover {
          // Visual
          text-shadow: 0 10px 20px rgba(0, 0, 0, 0.19),
            0 6px 6px rgba(0, 0, 0, 0.23);
          transform: rotate(360deg);
        }
      }
    }
  }

  .footer {
    // Position
    padding: 12px;
    padding-bottom: 0px;
  }
}
</style>
