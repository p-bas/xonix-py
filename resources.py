import logging
from pathlib import Path
import pygame
from enum import Enum


class ResourceLoader:
  def __init__(self):
    self.sounds_dir = Path(__file__).parent / "sounds"

  def load_sound(self, name: str, exts=(".wav", ".mp3")):
    """Try to load `name` with common extensions from the sounds folder.

    Returns a `pygame.mixer.Sound` instance or None if loading failed.
    """
    for ext in exts:
      p = self.sounds_dir / f"{name}{ext}"
      if p.exists():
        try:
          return pygame.mixer.Sound(str(p))
        except Exception as e:
          logging.warning("Failed to load sound %s: %s", p, e)
          return None
        
    logging.info("Sound '%s' not found in %s", name, self.sounds_dir)
    return None


class Sound(Enum):
  TICK = "ball"
  WIN = "win"
  FAIL = "fail"
  SCRATCH = "scratch"
  RUB = "rub"


class AudioManager:
  def __init__(self, loader: ResourceLoader = None, mixer_available=True, volume_map=None):
    self._loader = loader or ResourceLoader()
    self._mixer_available = mixer_available
    try:
      pygame.mixer.init()
    except Exception as e:
      logging.warning("pygame.mixer failed to initialize: %s", e)
      self._mixer_available = False

    # default volumes for supported sounds
    default_volumes = {
      Sound.TICK: 0.25,
      Sound.WIN: 0.7,
      Sound.FAIL: 0.5,
      Sound.SCRATCH: 0.3,
      Sound.RUB: 0.3,
    }

    self._volume_map = volume_map or default_volumes

    self._sounds = {}
    if self._mixer_available:
      for s in Sound:
        snd = self._loader.load_sound(s.value)
        self._sounds[s] = snd

      # apply configured volumes
      for s, vol in self._volume_map.items():
        try:
          self.set_volume(s, vol)
        except Exception:
          pass

  def get(self, sound: Sound):
    return self._sounds.get(sound)

  def play(self, sound: Sound) -> bool:
    if not self._mixer_available:
      return False
    snd = self.get(sound)
    if snd:
      try:
        snd.play()
        return True
      except Exception as e:
        logging.warning("Failed to play sound %s: %s", sound, e)
    return False

  def set_volume(self, sound: Sound, volume: float):
    snd = self.get(sound)
    if snd:
      try:
        snd.set_volume(volume)
      except Exception:
        pass
