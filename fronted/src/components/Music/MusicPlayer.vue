<template>
  <div class="music-player" @mouseover="showControls = true" @mouseleave="handleMouseLeave">
    <img :src="currentSong?.cover" alt="Cover" class="cover" @click="togglePlay" :style="coverRotationStyle"/>

    <transition name="fade">
      <div v-if="showControls" class="controls" @mouseenter="keepControlsVisible" @mouseleave="handleControlsLeave">
        <div class="lyrics-display">{{ currentLyrics }}</div>
        <div class="controls-row">
          <div class="progress-container">
            <input type="range" 
                   v-model="progress" 
                   :max="100" 
                   @input="seekSong" 
                   class="progress-bar" />
            <div class="time-display">{{ currentTime }} / {{ duration }}</div>
          </div>
          <div class="buttons">
            <button @click="prevSong" class="control-btn">⏮</button>
            <button @click="togglePlay" class="control-btn">
              {{ isPlaying ? '⏸' : '▶' }}
            </button>
            <button @click="nextSong" class="control-btn">⏭</button>
            <button @click="togglePlaylist" class="playlist-toggle-btn">
              <i class="iconfont icon-list" style="font-size: 14px;"></i>
            </button>
          </div>
        </div>

        <div v-if="showPlaylist" class="playlist">
          <div class="playlist-header">播放列表 ({{ playlist.length }})</div>
          <ul>
            <li v-for="(song, index) in playlist" 
                :key="index" 
                @click="playSong(index)"
                :class="{ active: currentIndex === index }">
              {{ song.title }}
            </li>
          </ul>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Howl } from 'howler';
import axios from 'axios';

const playlist = ref([
  { title: "星の奏でる歌", file: "http://localhost:8001/media/music/星の奏でる歌.mp3", cover: "http://localhost:8001/media/music/星の奏でる歌.jpeg", lyrics: "http://localhost:8001/media/music/星の奏でる歌.lrc" },
  { title: "雪の果てに君の名を", file: "http://localhost:8001/media/music/雪の果てに君の名を.mp3", cover: "http://localhost:8001/media/music/雪の果てに君の名を.jpg", lyrics: "http://localhost:8001/media/music/雪の果てに君の名を.lrc" },
]);

const currentIndex = ref(0);
const isPlaying = ref(false);
const showControls = ref(false);
const showPlaylist = ref(false);
const sound = ref(null);
const currentTime = ref('0:00');
const duration = ref('0:00');
const lyricsData = ref([]);
const currentLyrics = ref('加载中...');
const progress = ref(0);

const currentSong = computed(() => playlist.value[currentIndex.value] || {});

const keepControlsVisible = () => {
  showControls.value = true;
};

const handleControlsLeave = (event) => {
  if (!event.relatedTarget || !event.relatedTarget.closest('.music-player') && !event.relatedTarget.closest('.controls')) {
    showControls.value = false;
    showPlaylist.value = false;
  }
};

const togglePlaylist = () => {
  showPlaylist.value = !showPlaylist.value;
};

const coverRotationStyle = computed(() => ({
  animation: 'rotateCover 6s linear infinite',
  animationPlayState: isPlaying.value ? 'running' : 'paused',
}));

const parseLRC = (text) => {
  return text.split('\n')
    .map(line => {
      const match = line.match(/\[(\d+):(\d+\.\d+)\](.*)/);
      return match ? { time: parseInt(match[1]) * 60 + parseFloat(match[2]), text: match[3].trim() } : null;
    })
    .filter(Boolean)
    .sort((a, b) => a.time - b.time);
};

const loadLyrics = async () => {
  try {
    const { data } = await axios.get(currentSong.value.lyrics);
    lyricsData.value = parseLRC(data);
  } catch {
    lyricsData.value = [];
    currentLyrics.value = '暂无歌词';
  }
};

const updateLyrics = (currentTime) => {
  if (!lyricsData.value.length) return;
  
  for (let i = lyricsData.value.length - 1; i >= 0; i--) {
    if (currentTime >= lyricsData.value[i].time) {
      currentLyrics.value = lyricsData.value[i].text;
      break;
    }
  }
};

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60).toString().padStart(2, '0');
  return `${mins}:${secs}`;
};

const loadSong = () => {
  if (sound.value) {
    sound.value.unload();
  }

  // console.log(currentSong.value.file);

  sound.value = new Howl({
    src: [currentSong.value.file],
    html5: true,
    onplay: () => {
      isPlaying.value = true;
      updateTime();
    },
    onpause: () => {
      isPlaying.value = false;
    },
    onend: () => {
      nextSong();
    },
    onload: () => {
      duration.value = formatTime(sound.value.duration());
    }
  });

  sound.value.play();
  loadLyrics(); // 确保加载歌词
};

const updateTime = () => {
  if (!sound.value || !sound.value.playing()) return;

  const current = sound.value.seek() || 0;
  currentTime.value = formatTime(current);
  progress.value = (current / sound.value.duration()) * 100;
  updateLyrics(current);
  
  requestAnimationFrame(updateTime);
};

const seekSong = () => {
  if (!sound.value) return;
  const seekPosition = (progress.value / 100) * sound.value.duration();
  sound.value.seek(seekPosition);
  const current = sound.value.seek() || 0;
  currentTime.value = formatTime(current);
  updateLyrics(current);
  sound.value.play();
};

const togglePlay = () => {
  if (!sound.value) {
    loadSong();
  } else if (isPlaying.value) {
    sound.value.pause();
  } else {
    sound.value.play();
    updateTime();
  }
};

const nextSong = () => {
  currentIndex.value = (currentIndex.value + 1) % playlist.value.length;
  loadSong();
};

const prevSong = () => {
  currentIndex.value = (currentIndex.value - 1 + playlist.value.length) % playlist.value.length;
  loadSong();
};

const playSong = (index) => {
  currentIndex.value = index;
  loadSong();
};

const handleMouseEnter = () => {
  showControls.value = true;  // 鼠标进入时显示控制面板
};

const handleMouseLeave = (event) => {
  // 只有当鼠标离开封面图片和控制面板时，才隐藏控制面板
  if (!event.relatedTarget || !event.relatedTarget.closest('.music-player') && !event.relatedTarget.closest('.controls')) {
    showControls.value = false;
  }
};

onMounted(() => {
  loadLyrics();
});
</script>

<style>
.music-player {
  position: fixed;
  bottom: 20px;
  left: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: visible;
  transition: all 0.3s ease;
  z-index: 1000;
}

.cover {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 50%;
  cursor: pointer;
}

.controls {
  position: absolute;
  bottom: 0px;
  left: 60px;
  width: 420px;
  background: rgba(40, 40, 40, 0.95);
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.controls-row {
  display: flex;
  align-items: center;
}

.controls-row > *:not(:last-child) {
  margin-right: 6px;
}

.progress-container {
  width: 70%;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.progress-container input {
  width: 100%;
}

.buttons {
  flex-shrink: 0;
  display: flex;
  gap: 10px;
}

.lyrics-display {
  color: #fff;
  font-size: 14px;
}

.progress-bar {
  width: 80%;
  height: 6px;
  background: #444;
  appearance: none;
  border-radius: 3px;
}

.progress-bar::-webkit-slider-thumb {
  background: #2196F3;
  border-radius: 50%;
  width: 12px;
  height: 12px;
  appearance: none;
}

.time-display {
  color: #fff;
  font-size: 12px;
}

.control-btn {
  background: rgba(255,255,255,0.1);
  border: none;
  padding: 4px;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-btn:hover {
  background: rgba(255,255,255,0.2);
  transform: scale(1.1);
}

.playlist-toggle-btn {
  background: rgba(255,255,255,0.1);
  border: none;
  color: white;
  padding: 5px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
}

.playlist-toggle-btn:hover {
  background: rgba(255,255,255,0.2);
}

.playlist {
  position: absolute;
  bottom: 100px;
  /* left: 60px; */
  right: 0;
  width: 280px;
  background: rgba(40, 40, 40, 0.95);
  border-radius: 12px;
  max-height: 300px;
  overflow-y: auto;
}

.playlist li {
  font-size: 0.8em;
  padding: 5px 15px;
  color: #ccc;
  cursor: pointer;
  transition: all 0.2s ease;
}

.playlist li.active {
  color: #2196F3;
  font-weight: bold;
}

.playlist-header {
  margin-left: 5%;
  font-size: 1.2em;
  color: #e7e7e7;
}

@keyframes rotateCover {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
