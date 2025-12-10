from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from datetime import datetime


class PermissionType(Enum):
    MICROPHONE = "microphone"
    CAMERA = "camera"
    SENSORS = "sensors"
    LOCATION = "location"
    FULL_AI_MODE = "full_ai_mode"
    BACKGROUND_MONITORING = "background_monitoring"
    EMERGENCY_DETECTION = "emergency_detection"
    CLOUD_SYNC = "cloud_sync"
    APP_SCANNING = "app_scanning"
    INTERNET_SEARCH = "internet_search"


class PhoneSpecLevel(Enum):
    LOW_END = "low_end"
    MID_RANGE = "mid_range"
    HIGH_END = "high_end"


class ContextProfile(Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"
    GAMING = "gaming"
    CHARGING = "charging"
    LOW_BATTERY = "low_battery"
    WORK = "work"
    SOCIAL = "social"


class EmotionalState(Enum):
    HAPPY = "happy"
    CURIOUS = "curious"
    CONCERNED = "concerned"
    EXCITED = "excited"
    CALM = "calm"
    FOCUSED = "focused"
    PLAYFUL = "playful"
    PROTECTIVE = "protective"


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class FaceStyle(Enum):
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NEUTRAL = "neutral"
    CUTE = "cute"
    PROFESSIONAL = "professional"
    ANIMATED = "animated"


class SkinTone(Enum):
    LIGHT = "light"
    MEDIUM = "medium"
    DARK = "dark"
    NEUTRAL = "neutral"


class FacialExpression(Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SMILE = "smile"
    CURIOUS = "curious"
    CONCERNED = "concerned"
    EXCITED = "excited"
    CONFUSED = "confused"
    THINKING = "thinking"
    LISTENING = "listening"
    SPEAKING = "speaking"
    BLINKING = "blinking"
    NODDING = "nodding"


class VoiceStage(Enum):
    BABY = "baby"
    CHILD = "child"
    TEENAGE = "teenage"
    YOUNG_ADULT = "young_adult"
    MATURE = "mature"


class VoiceGender(Enum):
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NEUTRAL = "neutral"


class VoiceTone(Enum):
    SOFT = "soft"
    LIVELY = "lively"
    WARM = "warm"
    ENERGETIC = "energetic"
    CALM = "calm"
    GENTLE = "gentle"


class ExpressionIntensity(Enum):
    MINIMAL = "minimal"
    MODERATE = "moderate"
    ANIMATED = "animated"
    EXPRESSIVE = "expressive"


class NamingStatus(Enum):
    UNNAMED = "unnamed"
    AWAITING_NAME = "awaiting_name"
    NAMED = "named"
    NAME_CHANGING = "name_changing"


class NameChangeInitiator(Enum):
    USER_VOICE = "user_voice"
    USER_TEXT = "user_text"
    USER_SETTINGS = "user_settings"
    SYSTEM = "system"


class PersonaArchetype(Enum):
    FRIENDLY = "friendly"
    SERIOUS = "serious"
    PLAYFUL = "playful"
    CALM = "calm"
    ENERGETIC = "energetic"
    WISE = "wise"
    PROTECTIVE = "protective"
    CURIOUS = "curious"


@dataclass
class PhoneSpecifications:
    cpu_cores: int
    cpu_frequency_ghz: float
    ram_gb: int
    storage_gb: int
    has_gpu: bool
    gpu_type: Optional[str]
    os_type: str
    os_version: str
    has_microphone: bool
    has_camera: bool
    has_accelerometer: bool
    has_gyroscope: bool
    has_proximity_sensor: bool
    has_light_sensor: bool
    screen_refresh_rate_hz: int
    
    @property
    def capability_level(self) -> PhoneSpecLevel:
        score = (self.cpu_cores + self.ram_gb + (self.storage_gb / 100) + 
                (10 if self.has_gpu else 0))
        return (PhoneSpecLevel.LOW_END if score < 10 
                else PhoneSpecLevel.MID_RANGE if score < 20 
                else PhoneSpecLevel.HIGH_END)


@dataclass
class MemoryEntry:
    timestamp: datetime
    category: str
    content: str
    importance_score: float
    tags: List[str] = field(default_factory=list)
    related_memories: List[int] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "category": self.category,
            "content": self.content,
            "importance_score": self.importance_score,
            "tags": self.tags,
            "related_memories": self.related_memories
        }


@dataclass
class PersonalityTrait:
    name: str
    value: float
    influences: List[str] = field(default_factory=list)


@dataclass
class EmotionalProfile:
    trust_level: float
    affinity: float
    emotional_bond_strength: float
    dominant_emotion: EmotionalState
    emotional_memory: Dict[str, float] = field(default_factory=dict)
    shared_experiences: int = 0


@dataclass
class SensorData:
    timestamp: datetime
    accelerometer: Optional[Tuple[float, float, float]] = None
    gyroscope: Optional[Tuple[float, float, float]] = None
    proximity: Optional[float] = None
    light_level: Optional[float] = None
    audio_level: Optional[float] = None
    motion_detected: bool = False
    abnormal_motion: bool = False
    scream_detected: bool = False
    fall_detected: bool = False


@dataclass
class AppInfo:
    package_name: str
    display_name: str
    version: str
    install_date: datetime
    size_mb: float
    is_system_app: bool
    permissions_requested: List[str]
    last_used: datetime
    usage_time_minutes: int


@dataclass
class AppScanResult:
    app: AppInfo
    risk_level: str
    issues: List[str]
    recommendations: List[str]
    battery_impact: str


@dataclass
class PhoneHealthReport:
    timestamp: datetime
    cpu_usage_percent: float
    memory_usage_percent: float
    storage_usage_percent: float
    battery_percent: float
    temperature_celsius: float
    running_processes: int
    background_apps: int
    problematic_apps: List[str]
    optimization_suggestions: List[str]


@dataclass
class PermissionGrant:
    permission: PermissionType
    granted: bool
    granted_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None
    explicit_consent: bool = False


@dataclass
class InteractionLog:
    timestamp: datetime
    interaction_type: str
    content: str
    ai_response: str
    emotion_detected: Optional[str]
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    id: str
    severity: AlertSeverity
    title: str
    message: str
    timestamp: datetime
    action_required: bool
    suggested_action: Optional[str] = None
    dismissed: bool = False


@dataclass
class SearchQuery:
    query: str
    timestamp: datetime
    search_type: str
    results_count: int
    execution_time_ms: float
    cached: bool = False


@dataclass
class FacePreferences:
    style: FaceStyle = FaceStyle.NEUTRAL
    skin_tone: SkinTone = SkinTone.NEUTRAL
    expression_intensity: ExpressionIntensity = ExpressionIntensity.MODERATE
    eyes_open: bool = True
    show_eyebrows: bool = True
    eye_color: str = "blue"
    mouth_shape: str = "natural"
    custom_notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class VoicePreferences:
    gender: VoiceGender = VoiceGender.NEUTRAL
    base_tone: VoiceTone = VoiceTone.WARM
    pitch_offset: float = 0.0
    speed_offset: float = 0.0
    volume_level: float = 0.7
    enable_emotion_modulation: bool = True
    auto_voice_evolution: bool = True
    custom_tts_engine: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class FacialState:
    expression: FacialExpression = FacialExpression.NEUTRAL
    eye_position: Tuple[float, float] = (0.5, 0.5)
    mouth_opening: float = 0.0
    eyebrow_position: float = 0.5
    blink_rate: float = 0.3
    is_blinking: bool = False
    is_speaking: bool = False
    animation_frame: int = 0
    animation_speed: float = 1.0
    intensity: ExpressionIntensity = ExpressionIntensity.MODERATE
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class VoiceState:
    current_stage: VoiceStage = VoiceStage.BABY
    gender: VoiceGender = VoiceGender.NEUTRAL
    current_pitch: float = 1.0
    current_speed: float = 1.0
    current_tone: VoiceTone = VoiceTone.WARM
    emotional_pitch_shift: float = 0.0
    emotional_speed_shift: float = 0.0
    volume_level: float = 0.7
    is_speaking: bool = False
    current_text: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    age_days: int = 0


@dataclass
class GUIAsset:
    asset_id: str
    asset_type: str
    file_path: str
    format: str
    size_kb: float
    cached: bool = False
    last_used: datetime = field(default_factory=datetime.now)


@dataclass
class TTSProfile:
    profile_id: str
    stage: VoiceStage
    gender: VoiceGender
    base_pitch: float
    base_speed: float
    tone_description: str
    voice_file_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class GuiVoiceSyncEvent:
    event_id: str
    event_type: str
    facial_expression: FacialExpression
    voice_pitch: float
    voice_speed: float
    duration_ms: int
    text_to_speak: Optional[str] = None
    gesture_description: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class NameProfile:
    ai_name: Optional[str] = None
    user_name: Optional[str] = None
    naming_status: NamingStatus = NamingStatus.UNNAMED
    date_named: Optional[datetime] = None
    total_name_changes: int = 0
    last_name_change: Optional[datetime] = None
    last_name_changed_by: Optional[NameChangeInitiator] = None
    name_pronunciation_guide: Optional[str] = None
    emotional_attachment_to_name: float = 0.0
    use_name_in_greetings: bool = True
    use_name_in_conversations: bool = True
    use_user_name_in_responses: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def is_named(self) -> bool:
        return self.ai_name is not None and len(self.ai_name.strip()) > 0
    
    def is_user_known(self) -> bool:
        return self.user_name is not None and len(self.user_name.strip()) > 0


@dataclass
class NamingEvent:
    event_type: str
    ai_name: Optional[str] = None
    user_name: Optional[str] = None
    emotion_during_naming: Optional[str] = None
    user_satisfaction: Optional[float] = None
    context: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class PersonaFaceProfile:
    face_image_hash: Optional[str] = None
    skin_tone: Optional[str] = None
    eye_color: Optional[str] = None
    hair_color: Optional[str] = None
    hair_style: Optional[str] = None
    face_shape: Optional[str] = None
    distinctive_features: List[str] = field(default_factory=list)
    expression_style: str = "natural"
    uploaded_date: Optional[datetime] = None


@dataclass
class PersonaBehaviorProfile:
    primary_archetype: str = "neutral"
    secondary_archetype: Optional[str] = None
    likes: List[str] = field(default_factory=list)
    dislikes: List[str] = field(default_factory=list)
    habits: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    ideologies: List[str] = field(default_factory=list)
    tone_preference: str = "friendly"
    humor_style: str = "gentle"
    decision_style: str = "balanced"
    communication_style: str = "casual"
    problem_solving: str = "collaborative"
    personality_traits: Dict[str, float] = field(default_factory=dict)
    adoption_progress: float = 0.0
    created_date: Optional[datetime] = None


@dataclass
class PersonaVoiceProfile:
    base_tone: str = "neutral"
    speech_pace: str = "normal"
    formality: str = "casual"
    energy_level: str = "balanced"
    pitch_offset: float = 0.0
    emotional_expressiveness: float = 0.5


@dataclass
class PersonaProfile:
    is_set: bool = False
    face: PersonaFaceProfile = field(default_factory=PersonaFaceProfile)
    behavior: PersonaBehaviorProfile = field(default_factory=PersonaBehaviorProfile)
    voice: PersonaVoiceProfile = field(default_factory=PersonaVoiceProfile)
    interaction_count: int = 0
    adoption_progress: float = 0.0
    created_date: datetime = field(default_factory=datetime.now)
