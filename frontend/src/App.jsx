import { useEffect, useRef, useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000'

const SAMPLE_IMAGE =
  'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=900&q=85'

const AUDIO_TYPES = [
  'audio/mpeg',
  'audio/mp3',
  'audio/wav',
  'audio/x-wav',
  'audio/wave',
  'audio/ogg',
  'application/ogg',
  'audio/aac',
  'audio/mp4',
  'audio/x-m4a',
  'audio/m4a',
  'audio/webm',
  'video/webm',
  'audio/3gpp',
  'audio/3gpp2',
]

const Icon = ({ name, size = 20 }) => {
  const paths = {
    grid: (
      <>
        <rect x="3" y="3" width="7" height="7" rx="1.5" />
        <rect x="14" y="3" width="7" height="7" rx="1.5" />
        <rect x="3" y="14" width="7" height="7" rx="1.5" />
        <rect x="14" y="14" width="7" height="7" rx="1.5" />
      </>
    ),
    video: (
      <>
        <rect x="3" y="5" width="13" height="14" rx="2" />
        <path d="m16 10 5-3v10l-5-3" />
      </>
    ),
    folder: (
      <path d="M3 7a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
    ),
    settings: (
      <>
        <circle cx="12" cy="12" r="3" />
        <path d="m19.4 15 .1.1a2 2 0 1 1-2.8 2.8l-.1-.1a2 2 0 0 0-3.4 1.4v.3a2 2 0 1 1-4 0v-.2a2 2 0 0 0-3.4-1.4l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a2 2 0 0 0-1.4-3.4h-.3a2 2 0 1 1 0-4h.2a2 2 0 0 0 1.4-3.4l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a2 2 0 0 0 3.4-1.4v-.3a2 2 0 1 1 4 0v.2a2 2 0 0 0 3.4 1.4l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a2 2 0 0 0 1.4 3.4h.3a2 2 0 1 1 0 4h-.2a2 2 0 0 0-1.4 3.4z" />
      </>
    ),
    help: (
      <>
        <circle cx="12" cy="12" r="9" />
        <path d="M9.6 9a2.5 2.5 0 0 1 4.8 1c0 2-2.4 2-2.4 4" />
        <path d="M12 17h.01" />
      </>
    ),
    plus: <path d="M12 5v14M5 12h14" />,
    arrow: <path d="M7 17 17 7M7 7h10v10" />,
    play: <path d="m8 5 11 7-11 7z" />,
    image: (
      <>
        <rect x="3" y="3" width="18" height="18" rx="3" />
        <circle cx="8.5" cy="8.5" r="1.5" />
        <path d="m21 15-5-5L5 21" />
      </>
    ),
    clock: (
      <>
        <circle cx="12" cy="12" r="9" />
        <path d="M12 7v5l3 2" />
      </>
    ),
    sparkle: (
      <>
        <path d="m12 3 1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2z" />
        <path d="m19 14 1.2 2.8L23 18l-2.8 1.2L19 22l-1.2-2.8L15 18l2.8-1.2z" />
      </>
    ),
    chevron: <path d="m9 18 6-6-6-6" />,
    download: (
      <>
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <path d="m7 10 5 5 5-5M12 15V3" />
      </>
    ),
    music: (
      <>
        <path d="M9 18V5l12-2v13" />
        <circle cx="6" cy="18" r="3" />
        <circle cx="18" cy="16" r="3" />
      </>
    ),
    microphone: (
      <>
        <rect x="9" y="2" width="6" height="12" rx="3" />
        <path d="M5 10a7 7 0 0 0 14 0M12 17v5M8 22h8" />
      </>
    ),
    upload: (
      <>
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <path d="m17 8-5-5-5 5M12 3v12" />
      </>
    ),
    close: <path d="m18 6-12 12M6 6l12 12" />,
  }

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {paths[name]}
    </svg>
  )
}

const starterProjects = [
  {
    id: 1,
    name: 'The Modern Sanctuary',
    location: 'Sample property · Contemporary villa',
    image: SAMPLE_IMAGE,
    status: 'Sample',
    duration: '00:32',
  },
  {
    id: 2,
    name: 'A Little More Room to Dream',
    location: 'Sample property · Modern residence',
    image:
      'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=900&q=85',
    status: 'Sample',
    duration: '00:28',
  },
  {
    id: 3,
    name: 'Where Light Meets Living',
    location: 'Sample property · Luxury interiors',
    image:
      'https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=900&q=85',
    status: 'Sample',
    duration: '00:35',
  },
]

function App() {
  const [activeNav, setActiveNav] = useState('Overview')
  const [projects, setProjects] = useState(starterProjects)
  const [showCreator, setShowCreator] = useState(false)

  const [propertyName, setPropertyName] = useState('')
  const [location, setLocation] = useState('')
  const [price, setPrice] = useState('')
  const [propertyType, setPropertyType] = useState('Independent house')
  const [features, setFeatures] = useState('')
  const [contact, setContact] = useState('')

  const [selectedImages, setSelectedImages] = useState([])
  const [notice, setNotice] = useState('')
  const [noticeType, setNoticeType] = useState('success')
  const [isGenerating, setIsGenerating] = useState(false)
  const [storyboard, setStoryboard] = useState(null)
  const [generatedVideo, setGeneratedVideo] = useState(null)

  // AI Narration Studio state.
  const [narrationEnabled, setNarrationEnabled] = useState(true)
  const [narrationText, setNarrationText] = useState('')
  const [narrationVoice, setNarrationVoice] = useState(
    'en-IN-NeerjaNeural'
  )

  // Music Studio state.
  const [selectedAudio, setSelectedAudio] = useState(null)
  const [audioVolume, setAudioVolume] = useState(70)
  const [audioStartTime, setAudioStartTime] = useState(0)
  const [fadeIn, setFadeIn] = useState(1)
  const [fadeOut, setFadeOut] = useState(1.5)
  const [loopAudio, setLoopAudio] = useState(true)
  const [isRecording, setIsRecording] = useState(false)
  const [recordingSupported, setRecordingSupported] = useState(
    typeof window !== 'undefined' &&
      Boolean(navigator.mediaDevices?.getUserMedia) &&
      typeof MediaRecorder !== 'undefined'
  )

  const recorderRef = useRef(null)
  const streamRef = useRef(null)
  const chunksRef = useRef([])
  const audioUrlRef = useRef(null)
  const audioInputRef = useRef(null)
  const mountedRef = useRef(true)

  useEffect(() => {
    mountedRef.current = true

    return () => {
      mountedRef.current = false

      selectedImages.forEach((image) => {
        URL.revokeObjectURL(image.url)
      })

      if (audioUrlRef.current) {
        URL.revokeObjectURL(audioUrlRef.current)
      }

      if (recorderRef.current?.state === 'recording') {
        recorderRef.current.ondataavailable = null
        recorderRef.current.onstop = null

        try {
          recorderRef.current.stop()
        } catch {
          // The recorder may already have stopped.
        }
      }

      streamRef.current?.getTracks().forEach((track) => track.stop())
    }

    // The URLs are cleaned up when the component unmounts.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const showNotice = (message, type = 'success') => {
    setNotice(message)
    setNoticeType(type)
  }

  const openCreator = () => {
    setNotice('')
    setShowCreator(true)
    setActiveNav('Create video')
  }

  const closeCreator = () => {
    setShowCreator(false)
    setActiveNav('Overview')
  }

  const goToOverview = () => {
    setShowCreator(false)
    setActiveNav('Overview')
    setNotice('')
  }

  const handleImageChange = (event) => {
    const files = Array.from(event.target.files || [])

    const validFiles = files.filter((file) =>
      ['image/jpeg', 'image/png', 'image/webp'].includes(file.type)
    )

    const remaining = Math.max(0, 8 - selectedImages.length)
    const nextFiles = validFiles.slice(0, remaining)

    setSelectedImages((current) => [
      ...current,
      ...nextFiles.map((file) => ({
        file,
        url: URL.createObjectURL(file),
        id: `${file.name}-${file.lastModified}-${Math.random()}`,
      })),
    ])

    if (files.length !== validFiles.length) {
      showNotice('Only JPG, PNG, and WEBP images are supported.', 'error')
    } else if (validFiles.length > remaining) {
      showNotice('You can upload a maximum of 8 photos.', 'error')
    } else {
      setNotice('')
    }

    event.target.value = ''
  }

  const removeImage = (id) => {
    setSelectedImages((current) => {
      const removed = current.find((image) => image.id === id)

      if (removed) {
        URL.revokeObjectURL(removed.url)
      }

      return current.filter((image) => image.id !== id)
    })
  }

  // Replace the currently selected audio and release its previous preview URL.
  const setAudioFile = (file, source = 'upload') => {
    if (!file) return

    const validType =
      AUDIO_TYPES.includes(file.type) ||
      /\.(mp3|wav|ogg|aac|m4a|webm)$/i.test(file.name)

    if (!validType) {
      showNotice(
        'Choose an MP3, WAV, OGG, AAC, M4A, or WebM audio file.',
        'error'
      )
      return
    }

    if (file.size > 30 * 1024 * 1024) {
      showNotice('Audio files must be 30 MB or smaller.', 'error')
      return
    }

    if (audioUrlRef.current) {
      URL.revokeObjectURL(audioUrlRef.current)
    }

    const url = URL.createObjectURL(file)
    audioUrlRef.current = url

    setSelectedAudio({
      file,
      url,
      source,
      name: file.name,
      size: file.size,
    })

    showNotice(
      source === 'recording'
        ? 'Your recording is ready to use in the property video.'
        : `${file.name} added to your Music Studio.`,
      'success'
    )
  }

  const handleAudioChange = (event) => {
    const file = event.target.files?.[0]

    if (file) {
      setAudioFile(file, 'upload')
    }

    event.target.value = ''
  }

  const startRecording = async () => {
    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) {
      setRecordingSupported(false)
      showNotice(
        'Audio recording is not supported in this browser. Try an up-to-date version of Chrome or Safari.',
        'error'
      )
      return
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      })

      streamRef.current = stream
      chunksRef.current = []

      const preferredMimeType = [
        'audio/webm;codecs=opus',
        'audio/webm',
        'audio/mp4',
      ].find((type) => MediaRecorder.isTypeSupported(type))

      const recorder = preferredMimeType
        ? new MediaRecorder(stream, { mimeType: preferredMimeType })
        : new MediaRecorder(stream)

      recorderRef.current = recorder

      recorder.ondataavailable = (event) => {
        if (event.data?.size > 0) {
          chunksRef.current.push(event.data)
        }
      }

      recorder.onerror = () => {
        showNotice('Something went wrong while recording audio.', 'error')
      }

      recorder.onstop = () => {
        const mimeType = recorder.mimeType || 'audio/webm'
        const extension = mimeType.includes('mp4') ? 'm4a' : 'webm'

        const recording = new File(
          chunksRef.current,
          `dwellreel-recording.${extension}`,
          { type: mimeType }
        )

        stream.getTracks().forEach((track) => track.stop())

        if (streamRef.current === stream) {
          streamRef.current = null
        }

        if (mountedRef.current && recording.size > 0) {
          setAudioFile(recording, 'recording')
        }
      }

      recorder.start(250)
      setIsRecording(true)
      showNotice('Recording started. Speak into your microphone.', 'info')
    } catch (error) {
      console.error('Microphone access failed:', error)

      showNotice(
        'Microphone access was denied or unavailable. Allow microphone access in your browser settings and try again.',
        'error'
      )
    }
  }

  const stopRecording = () => {
    const recorder = recorderRef.current

    if (recorder && recorder.state !== 'inactive') {
      recorder.stop()
    }

    setIsRecording(false)
  }

  const removeAudio = () => {
    if (isRecording) {
      stopRecording()
    }

    if (audioUrlRef.current) {
      URL.revokeObjectURL(audioUrlRef.current)
      audioUrlRef.current = null
    }

    setSelectedAudio(null)
    showNotice('Background audio removed.', 'info')
  }

  const handleCreateProject = async (event) => {
    event.preventDefault()
    setNotice('')

    if (isGenerating) return

    if (!propertyName.trim() || !location.trim() || !price.trim()) {
      showNotice(
        'Please enter the property name, location, and asking price.',
        'error'
      )
      return
    }

    if (selectedImages.length < 4 || selectedImages.length > 8) {
      showNotice('Please upload between 4 and 8 property photos.', 'error')
      return
    }

    if (isRecording) {
      showNotice('Please stop your audio recording before generating.', 'error')
      return
    }

    if (narrationText.trim().length > 5000) {
      showNotice('Narration script must be 5000 characters or fewer.', 'error')
      return
    }

    const featureList = features
      .split(/[,\n]+/)
      .map((feature) => feature.trim())
      .filter(Boolean)

    try {
      setIsGenerating(true)
      setStoryboard(null)
      setGeneratedVideo(null)

      showNotice(
        narrationEnabled
          ? 'Creating your AI voice narration and preparing your property video…'
          : selectedAudio
            ? 'Uploading your property photos and background music, then rendering your video…'
            : 'Uploading your property photos and preparing your video…'
      )

      const formData = new FormData()

      formData.append('property_name', propertyName.trim())
      formData.append('location', location.trim())
      formData.append('price', price.trim())
      formData.append('property_type', propertyType)
      formData.append('features', featureList.join(', '))
      formData.append('contact', contact.trim())
      formData.append('call_to_action', 'Enquire today')

      // AI narration settings.
      formData.append('narration_enabled', String(narrationEnabled))
      formData.append('narration_text', narrationText.trim())
      formData.append('narration_voice', narrationVoice)

      // Background music settings.
      formData.append('audio_volume', String(audioVolume / 100))
      formData.append('audio_start_time', String(audioStartTime))
      formData.append('fade_in', String(fadeIn))
      formData.append('fade_out', String(fadeOut))
      formData.append('loop_audio', String(loopAudio))

      selectedImages.forEach((image) => {
        formData.append('photos', image.file)
      })

      if (selectedAudio) {
        formData.append(
          'audio',
          selectedAudio.file,
          selectedAudio.file.name
        )
      }

      const response = await fetch(`${API_URL}/api/generate-video`, {
        method: 'POST',
        body: formData,
      })

      const result = await response.json().catch(() => ({}))

      if (!response.ok) {
        const message =
          typeof result.detail === 'string'
            ? result.detail
            : `The server returned an error (${response.status}).`

        throw new Error(message)
      }

      if (!result.storyboard || !result.video?.video_url) {
        throw new Error(
          'The server responded, but the generated video URL was missing.'
        )
      }

      const video = {
        filename: result.video.filename,
        url: result.video.video_url,
        downloadUrl:
          result.video.download_url ||
          `${API_URL}/api/download/${encodeURIComponent(
            result.video.filename
          )}`,
      }

      setStoryboard(result.storyboard)
      setGeneratedVideo(video)

      const audioDetails = []

      if (result.narration_included) {
        audioDetails.push('AI narration included')
      }

      if (result.audio_included && selectedAudio) {
        audioDetails.push('background music included')
      }

      showNotice(
        `Your property video is ready! ${
          result.scene_count ?? result.storyboard.scene_count ?? 0
        } scenes · ${
          result.duration_seconds ??
          result.storyboard.total_duration_seconds ??
          0
        } seconds${
          audioDetails.length
            ? ` · ${audioDetails.join(' + ')}`
            : ''
        }.`,
        'success'
      )
    } catch (error) {
      console.error('Video generation failed:', error)

      showNotice(
        error.message ||
          'Could not connect to DwellReel AI. Check that the backend is running.',
        'error'
      )
    } finally {
      setIsGenerating(false)
    }
  }

  const saveStoryboardProject = () => {
    if (!storyboard) return

    const project = {
      id: Date.now(),
      name: storyboard.property_name,
      location: `${storyboard.location || location} · ${propertyType}`,
      image: selectedImages[0]?.url || SAMPLE_IMAGE,
      status: generatedVideo ? 'Video ready' : 'Storyboard ready',
      duration: formatDuration(storyboard.total_duration_seconds),
      storyboard,
      videoUrl: generatedVideo?.url || null,
      videoDownloadUrl: generatedVideo?.downloadUrl || null,
      videoFilename: generatedVideo?.filename || null,
    }

    setProjects((current) => [
      project,
      ...current.filter((item) => item.id !== project.id),
    ])

    showNotice(
      generatedVideo
        ? 'Your property video has been added to My Projects.'
        : 'Your storyboard has been added to My Projects.',
      'success'
    )
  }

  const openSavedProject = (project) => {
    if (!project.storyboard) {
      showNotice(
        'This is an inspiration example. Create your own property video to get started.',
        'info'
      )
      return
    }

    setStoryboard(project.storyboard)

    setGeneratedVideo(
      project.videoUrl
        ? {
            url: project.videoUrl,
            downloadUrl:
              project.videoDownloadUrl ||
              `${API_URL}/api/download/${encodeURIComponent(
                project.videoFilename || ''
              )}`,
            filename: project.videoFilename,
          }
        : null
    )

    setPropertyName(project.storyboard.property_name || project.name)
    setLocation(project.storyboard.location || '')
    setShowCreator(true)
    setActiveNav('Create video')
    setNotice('')
  }

  const visibleProjects =
    activeNav === 'My projects'
      ? projects.filter((project) => project.status !== 'Sample')
      : projects

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <button className="brand" onClick={goToOverview}>
          <span className="brand-mark">
            <span />
            <span />
            <span />
          </span>

          <span className="brand-name">
            dwellreel<span>AI</span>
          </span>
        </button>

        <div className="workspace-label">WORKSPACE</div>

        <nav className="sidebar-nav" aria-label="Main navigation">
          <button
            className={`nav-item ${activeNav === 'Overview' ? 'active' : ''}`}
            onClick={goToOverview}
          >
            <Icon name="grid" />
            <span>Overview</span>
          </button>

          <button
            className={`nav-item ${
              activeNav === 'Create video' ? 'active' : ''
            }`}
            onClick={openCreator}
          >
            <Icon name="video" />
            <span>Create a video</span>
            <span className="nav-add">
              <Icon name="plus" size={15} />
            </span>
          </button>

          <button
            className={`nav-item ${
              activeNav === 'My projects' ? 'active' : ''
            }`}
            onClick={() => {
              setActiveNav('My projects')
              setShowCreator(false)
              setNotice('')
            }}
          >
            <Icon name="folder" />
            <span>My projects</span>
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-tip">
            <div className="tip-icon">
              <Icon name="sparkle" size={19} />
            </div>

            <p className="tip-title">Every property has a story.</p>
            <p className="tip-copy">Let yours be seen.</p>

            <button onClick={openCreator}>
              Create your first reel <Icon name="arrow" size={14} />
            </button>
          </div>

          <button
            className="nav-item"
            onClick={() =>
              showNotice(
                'Settings will be available in a future version.',
                'info'
              )
            }
          >
            <Icon name="settings" />
            <span>Settings</span>
          </button>

          <button
            className="nav-item"
            onClick={() =>
              showNotice(
                'Help center coming soon. Follow the creator form guidance for now.',
                'info'
              )
            }
          >
            <Icon name="help" />
            <span>Help & support</span>
          </button>

          <div className="profile">
            <div className="avatar">DR</div>

            <div className="profile-text">
              <strong>Your workspace</strong>
              <span>Property creator</span>
            </div>

            <span className="profile-menu">···</span>
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumbs">
            <span>Workspace</span>
            <Icon name="chevron" size={14} />
            <strong>{showCreator ? 'Create a video' : activeNav}</strong>
          </div>

          <div className="topbar-right">
            <span className="status-dot" />
            <span className="status-label">Creative studio</span>
            <div className="topbar-avatar">DR</div>
          </div>
        </header>

        <div className="page-content">
          {notice && (
            <div
              className={`notice-banner ${
                noticeType === 'error' ? 'notice-error' : ''
              }`}
              role="status"
            >
              <span>{notice}</span>
              <button
                onClick={() => setNotice('')}
                aria-label="Dismiss notification"
              >
                ×
              </button>
            </div>
          )}

          {showCreator ? (
            <section className="creator-page">
              <button className="back-link" onClick={closeCreator}>
                ← Back to overview
              </button>

              <div className="page-heading">
                <div>
                  <div className="eyebrow">
                    <Icon name="sparkle" size={15} />
                    YOUR NEXT LISTING, REIMAGINED
                  </div>

                  <h1>
                    Let's tell its <span>story.</span>
                  </h1>

                  <p>
                    Bring your property details, best photos, and soundtrack.
                    We'll help you shape them into a reel worth watching.
                  </p>
                </div>

                <div className="step-indicator">
                  <span>01</span>
                  <div />
                  <span>02</span>
                  <div />
                  <span>03</span>
                </div>
              </div>

              <form className="creator-layout" onSubmit={handleCreateProject}>
                <div className="form-column">
                  {/* PROPERTY DETAILS */}

                  <section className="form-card">
                    <div className="card-heading">
                      <span className="section-number">01</span>

                      <div>
                        <h2>Property essentials</h2>
                        <p>The facts behind the feeling.</p>
                      </div>
                    </div>

                    <div className="form-grid">
                      <label className="field full-field">
                        <span>
                          Property name <b>*</b>
                        </span>

                        <input
                          value={propertyName}
                          onChange={(event) =>
                            setPropertyName(event.target.value)
                          }
                          placeholder="e.g. The Willow House"
                          required
                        />
                      </label>

                      <label className="field">
                        <span>
                          Location <b>*</b>
                        </span>

                        <input
                          value={location}
                          onChange={(event) =>
                            setLocation(event.target.value)
                          }
                          placeholder="City, neighbourhood"
                          required
                        />
                      </label>

                      <label className="field">
                        <span>
                          Asking price <b>*</b>
                        </span>

                        <input
                          value={price}
                          onChange={(event) => setPrice(event.target.value)}
                          placeholder="e.g. ₹1.25 Cr"
                          required
                        />
                      </label>

                      <label className="field full-field">
                        <span>Property type</span>

                        <select
                          value={propertyType}
                          onChange={(event) =>
                            setPropertyType(event.target.value)
                          }
                        >
                          <option>Independent house</option>
                          <option>Apartment</option>
                          <option>Villa</option>
                          <option>Penthouse</option>
                          <option>Studio</option>
                          <option>Commercial property</option>
                          <option>Plot / land</option>
                        </select>
                      </label>

                      <label className="field full-field">
                        <span>What makes it special?</span>

                        <textarea
                          value={features}
                          onChange={(event) =>
                            setFeatures(event.target.value)
                          }
                          placeholder="e.g. 3 bedrooms, sunlit living room, private garden..."
                          rows={4}
                        />

                        <small>
                          Share only verified details. Separate features with
                          commas or new lines.
                        </small>
                      </label>

                      <label className="field full-field">
                        <span>Contact details (optional)</span>

                        <input
                          value={contact}
                          onChange={(event) =>
                            setContact(event.target.value)
                          }
                          placeholder="Phone number or email"
                        />

                        <small>
                          Contact details are sent to the backend.
                        </small>
                      </label>
                    </div>
                  </section>

                  {/* PROPERTY PHOTOS */}

                  <section className="form-card">
                    <div className="card-heading">
                      <span className="section-number">02</span>

                      <div>
                        <h2>Bring in the visuals</h2>
                        <p>
                          Choose 4–8 photos that show the property at its best.
                        </p>
                      </div>
                    </div>

                    <label className="upload-zone">
                      <input
                        type="file"
                        accept="image/jpeg,image/png,image/webp"
                        multiple
                        onChange={handleImageChange}
                      />

                      <span className="upload-icon">
                        <Icon name="image" size={24} />
                      </span>

                      <strong>
                        Drop your photos here, or <em>browse files</em>
                      </strong>

                      <span className="upload-meta">
                        JPG, PNG, WEBP · Up to 8 images
                      </span>
                    </label>

                    {selectedImages.length > 0 && (
                      <div className="selected-images">
                        {selectedImages.map((image, index) => (
                          <div className="selected-image" key={image.id}>
                            <img
                              src={image.url}
                              alt={`Selected property ${index + 1}`}
                            />

                            <span>{index + 1}</span>

                            <button
                              type="button"
                              onClick={() => removeImage(image.id)}
                              aria-label={`Remove image ${index + 1}`}
                            >
                              ×
                            </button>
                          </div>
                        ))}
                      </div>
                    )}

                    <div className="upload-footer">
                      <span>{selectedImages.length} of 8 photos added</span>
                      <span>Minimum 4 photos</span>
                    </div>
                  </section>

                  {/* AI NARRATION STUDIO */}

                  <section className="form-card narration-studio">
                    <div className="card-heading">
                      <span className="section-number">
                        <Icon name="microphone" size={19} />
                      </span>

                      <div>
                        <h2>AI Narration Studio</h2>
                        <p>
                          Give your property a voice with natural AI
                          storytelling.
                        </p>
                      </div>
                    </div>

                    <div className="narration-toggle-row">
                      <div>
                        <strong>AI voice narration</strong>
                        <p>
                          Automatically narrate your property video.
                        </p>
                      </div>

                      <label className="narration-switch">
                        <input
                          type="checkbox"
                          checked={narrationEnabled}
                          onChange={(event) =>
                            setNarrationEnabled(event.target.checked)
                          }
                          disabled={isGenerating}
                        />

                        <span className="narration-switch-slider" />
                      </label>
                    </div>

                    {narrationEnabled && (
                      <>
                        <div className="narration-voice-section">
                          <label className="field">
                            <span>Select narration voice</span>

                            <select
                              value={narrationVoice}
                              onChange={(event) =>
                                setNarrationVoice(event.target.value)
                              }
                              disabled={isGenerating}
                            >
                              <optgroup label="Indian English">
                                <option value="en-IN-NeerjaNeural">
                                  Neerja · Female
                                </option>

                                <option value="en-IN-PrabhatNeural">
                                  Prabhat · Male
                                </option>
                              </optgroup>

                              <optgroup label="American English">
                                <option value="en-US-AriaNeural">
                                  Aria · Female
                                </option>

                                <option value="en-US-GuyNeural">
                                  Guy · Male
                                </option>
                              </optgroup>

                              <optgroup label="Hindi">
                                <option value="hi-IN-SwaraNeural">
                                  Swara · Female
                                </option>

                                <option value="hi-IN-MadhurNeural">
                                  Madhur · Male
                                </option>
                              </optgroup>
                            </select>
                          </label>
                        </div>

                        <div className="narration-script-section">
                          <label className="field">
                            <span>
                              Custom narration script (optional)
                            </span>

                            <textarea
                              value={narrationText}
                              onChange={(event) =>
                                setNarrationText(event.target.value)
                              }
                              placeholder="Write your own property narration here. Leave this empty and AI will automatically create a script using your property details."
                              rows={5}
                              maxLength={5000}
                              disabled={isGenerating}
                            />

                            <small>
                              {narrationText.length}/5000 characters. Leave
                              empty for automatically generated property
                              narration.
                            </small>
                          </label>
                        </div>

                        <div className="narration-info">
                          <Icon name="sparkle" size={17} />

                          <p>
                            Your narration will be generated using the
                            property information you provide. Background
                            music will be mixed underneath your voice.
                          </p>
                        </div>
                      </>
                    )}

                    {!narrationEnabled && (
                      <p className="audio-helper">
                        AI narration is disabled. Your video can still
                        include background music from Music Studio.
                      </p>
                    )}
                  </section>

                  {/* MUSIC STUDIO */}

                  <section className="form-card music-studio">
                    <div className="card-heading">
                      <span className="section-number">
                        <Icon name="music" size={19} />
                      </span>

                      <div>
                        <h2>Music Studio</h2>
                        <p>
                          Give your property reel its own soundtrack.
                        </p>
                      </div>
                    </div>

                    <div className="music-studio-intro">
                      <div className="music-artwork">
                        <Icon name="music" size={30} />
                      </div>

                      <div>
                        <strong>
                          {selectedAudio
                            ? selectedAudio.name
                            : 'Your soundtrack starts here'}
                        </strong>

                        <p>
                          {selectedAudio
                            ? `${
                                selectedAudio.source === 'recording'
                                  ? 'Your recording'
                                  : 'Audio file'
                              } · ${(
                                selectedAudio.size /
                                (1024 * 1024)
                              ).toFixed(2)} MB`
                            : 'Upload a track or record your own voice.'}
                        </p>
                      </div>

                      {selectedAudio && (
                        <button
                          className="audio-remove-button"
                          type="button"
                          onClick={removeAudio}
                          aria-label="Remove background audio"
                          title="Remove audio"
                        >
                          <Icon name="close" size={17} />
                        </button>
                      )}
                    </div>

                    <div className="music-action-grid">
                      <button
                        className="music-action-button"
                        type="button"
                        onClick={() => audioInputRef.current?.click()}
                        disabled={isGenerating || isRecording}
                      >
                        <Icon name="upload" size={21} />
                        <strong>Upload audio</strong>
                        <span>Choose a file</span>
                      </button>

                      <button
                        className="music-action-button"
                        type="button"
                        onClick={
                          isRecording ? stopRecording : startRecording
                        }
                        disabled={isGenerating || !recordingSupported}
                      >
                        <Icon name="microphone" size={21} />

                        <strong>
                          {isRecording
                            ? 'Stop recording'
                            : 'Record voice'}
                        </strong>

                        <span>
                          {isRecording
                            ? 'Recording in progress'
                            : 'Use your microphone'}
                        </span>
                      </button>
                    </div>

                    <input
                      ref={audioInputRef}
                      type="file"
                      accept=".mp3,.wav,.ogg,.aac,.m4a,.webm,audio/*"
                      onChange={handleAudioChange}
                      hidden
                    />

                    {isRecording && (
                      <div className="recording-indicator" role="status">
                        <span className="recording-dot" />
                        Recording in progress. Select Stop recording when
                        you're finished.
                      </div>
                    )}

                    {selectedAudio && (
                      <div className="audio-preview">
                        <label className="audio-preview-label">
                          <Icon name="play" size={16} />
                          Preview your soundtrack
                        </label>

                        <audio
                          key={selectedAudio.url}
                          src={selectedAudio.url}
                          controls
                          preload="metadata"
                          className="audio-player"
                        >
                          Your browser does not support audio playback.
                        </audio>
                      </div>
                    )}

                    <div className="music-divider" />

                    <div className="audio-control-heading">
                      <h3>Sound settings</h3>
                      <span>Applied when generating your MP4</span>
                    </div>

                    <div className="audio-control">
                      <div className="audio-control-label">
                        <label htmlFor="audio-volume">
                          Background music volume
                        </label>

                        <strong>{audioVolume}%</strong>
                      </div>

                      <input
                        id="audio-volume"
                        type="range"
                        min="0"
                        max="100"
                        step="5"
                        value={audioVolume}
                        onChange={(event) =>
                          setAudioVolume(Number(event.target.value))
                        }
                        disabled={isGenerating}
                      />

                      <div className="range-endpoints">
                        <span>Muted</span>
                        <span>Maximum</span>
                      </div>
                    </div>

                    <div className="audio-control">
                      <div className="audio-control-label">
                        <label htmlFor="audio-start">
                          Start audio at
                        </label>

                        <strong>{audioStartTime}s</strong>
                      </div>

                      <input
                        id="audio-start"
                        type="range"
                        min="0"
                        max="60"
                        step="1"
                        value={audioStartTime}
                        onChange={(event) =>
                          setAudioStartTime(Number(event.target.value))
                        }
                        disabled={isGenerating}
                      />

                      <div className="range-endpoints">
                        <span>Beginning</span>
                        <span>60 seconds</span>
                      </div>
                    </div>

                    <div className="audio-two-column">
                      <label className="field">
                        <span>Fade in (seconds)</span>

                        <input
                          type="number"
                          min="0"
                          max="30"
                          step="0.5"
                          value={fadeIn}
                          onChange={(event) =>
                            setFadeIn(
                              Math.min(
                                30,
                                Math.max(0, Number(event.target.value) || 0)
                              )
                            )
                          }
                          disabled={isGenerating}
                        />
                      </label>

                      <label className="field">
                        <span>Fade out (seconds)</span>

                        <input
                          type="number"
                          min="0"
                          max="30"
                          step="0.5"
                          value={fadeOut}
                          onChange={(event) =>
                            setFadeOut(
                              Math.min(
                                30,
                                Math.max(0, Number(event.target.value) || 0)
                              )
                            )
                          }
                          disabled={isGenerating}
                        />
                      </label>
                    </div>

                    <label className="audio-checkbox">
                      <input
                        type="checkbox"
                        checked={loopAudio}
                        onChange={(event) =>
                          setLoopAudio(event.target.checked)
                        }
                        disabled={isGenerating}
                      />

                      <span className="audio-checkbox-copy">
                        <strong>Loop background music</strong>

                        <small>
                          Repeat the selected track to cover the video
                          duration.
                        </small>
                      </span>
                    </label>

                    {!selectedAudio && (
                      <p className="audio-helper">
                        No soundtrack selected. Your video will be generated
                        without background audio.
                      </p>
                    )}

                    <p className="audio-helper">
                      Only use audio you own or have permission to use.
                    </p>
                  </section>

                  {/* GENERATE VIDEO */}

                  <button
                    className="primary-button submit-button"
                    type="submit"
                    disabled={isGenerating || isRecording}
                  >
                    <Icon name="sparkle" size={18} />

                    {isGenerating
                      ? 'Generating your property video...'
                      : 'Generate my property video'}

                    {!isGenerating && <Icon name="arrow" size={17} />}
                  </button>

                  {isGenerating && (
                    <div
                      className="form-card generation-progress"
                      role="status"
                    >
                      <div className="card-heading">
                        <span className="section-number">
                          <Icon name="clock" size={17} />
                        </span>

                        <div>
                          <h2>Your property is getting its moment</h2>

                          <p>
                            Uploading photos and rendering your video. Keep
                            this page open while generation finishes.
                          </p>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* GENERATED STORYBOARD */}

                  {storyboard && (
                    <section className="form-card generated-storyboard">
                      <div className="card-heading">
                        <span className="section-number">
                          <Icon name="sparkle" size={17} />
                        </span>

                        <div>
                          <h2>
                            {generatedVideo
                              ? 'Your property video is ready!'
                              : 'Your storyboard is ready'}
                          </h2>

                          <p>
                            Review your generated scenes and watch your reel.
                          </p>
                        </div>
                      </div>

                      <div className="storyboard-summary">
                        <div>
                          <strong>{storyboard.scene_count}</strong>
                          <span>Scenes</span>
                        </div>

                        <div>
                          <strong>
                            {storyboard.total_duration_seconds}s
                          </strong>
                          <span>Duration</span>
                        </div>

                        <div>
                          <strong>9:16</strong>
                          <span>Vertical format</span>
                        </div>
                      </div>

                      {generatedVideo && (
                        <div className="generated-video-result">
                          <h3>Your finished property reel</h3>

                          <video
                            className="generated-video-player"
                            src={generatedVideo.url}
                            controls
                            playsInline
                            preload="metadata"
                          >
                            Your browser does not support HTML video.
                          </video>

                          <div className="video-result-actions">
                            <a
                              className="primary-button"
                              href={
                                generatedVideo.downloadUrl ||
                                generatedVideo.url
                              }
                              download={
                                generatedVideo.filename ||
                                'dwellreel-video.mp4'
                              }
                            >
                              <Icon name="download" size={17} />
                              Download MP4
                            </a>

                            <a
                              className="secondary-button"
                              href={generatedVideo.url}
                              target="_blank"
                              rel="noreferrer"
                            >
                              Open video <Icon name="arrow" size={15} />
                            </a>
                          </div>

                          <p className="video-file-name">
                            {generatedVideo.filename}
                          </p>
                        </div>
                      )}

                      <div className="generated-scenes">
                        {(storyboard.scenes || []).map((scene) => {
                          const imageIndex =
                            Math.max(0, scene.scene - 1) %
                            Math.max(1, selectedImages.length)

                          const sceneImage = selectedImages[imageIndex]

                          return (
                            <article
                              className="generated-scene"
                              key={scene.scene}
                            >
                              <div className="generated-scene-image">
                                {sceneImage && (
                                  <img
                                    src={sceneImage.url}
                                    alt={`Scene ${scene.scene}`}
                                  />
                                )}

                                <span>
                                  {String(scene.scene).padStart(2, '0')}
                                </span>
                              </div>

                              <div className="generated-scene-copy">
                                <span className="scene-purpose">
                                  {(scene.purpose || 'scene').replace(
                                    /_/g,
                                    ' '
                                  )}
                                </span>

                                <h3>{scene.headline}</h3>
                                <p>{scene.caption}</p>

                                <small>
                                  <Icon name="clock" size={13} />{' '}
                                  {scene.duration} seconds
                                </small>
                              </div>
                            </article>
                          )
                        })}
                      </div>

                      <div className="storyboard-actions">
                        <button
                          type="button"
                          className="primary-button"
                          onClick={saveStoryboardProject}
                        >
                          <Icon name="folder" size={17} />
                          Save to my projects
                        </button>

                        <p>
                          {generatedVideo
                            ? 'Your MP4 is ready to preview and download.'
                            : 'Your storyboard is ready, but no MP4 is available yet.'}
                        </p>
                      </div>
                    </section>
                  )}
                </div>

                {/* PREVIEW COLUMN */}

                <aside className="preview-column">
                  <div className="preview-card">
                    <div className="preview-card-top">
                      <span>
                        {generatedVideo
                          ? 'GENERATED PROPERTY VIDEO'
                          : 'YOUR STORYBOARD'}
                      </span>

                      <span className="live-pill">
                        <i />
                        {isGenerating
                          ? 'WORKING'
                          : generatedVideo
                            ? 'VIDEO READY'
                            : storyboard
                              ? 'READY'
                              : 'DRAFT'}
                      </span>
                    </div>

                    <div className="preview-image-wrap">
                      {generatedVideo ? (
                        <video
                          className="preview-image"
                          src={generatedVideo.url}
                          controls
                          playsInline
                          preload="metadata"
                        >
                          Your browser does not support HTML video.
                        </video>
                      ) : (
                        <>
                          {selectedImages.length > 0 ? (
                            <img
                              src={selectedImages[0].url}
                              alt="Property preview"
                              className="preview-image"
                            />
                          ) : (
                            <div className="preview-placeholder">
                              <div className="placeholder-art">
                                <Icon name="image" size={34} />
                              </div>

                              <span>Your first frame</span>

                              <small>
                                Beautiful things start with a photo.
                              </small>
                            </div>
                          )}

                          <div className="preview-overlay">
                            <span className="preview-kicker">
                              A DWELLREEL PRODUCTION
                            </span>

                            <h3>
                              {propertyName || 'Your next great listing'}
                            </h3>

                            <p>{location || 'Your property location'}</p>

                            {price && <strong>{price}</strong>}
                          </div>

                          <div className="play-button">
                            <Icon name="play" size={20} />
                          </div>
                        </>
                      )}

                      <span className="preview-duration">
                        {storyboard
                          ? formatDuration(storyboard.total_duration_seconds)
                          : '00:30'}
                      </span>
                    </div>

                    {generatedVideo && (
                      <a
                        className="primary-button preview-download"
                        href={
                          generatedVideo.downloadUrl || generatedVideo.url
                        }
                        download={
                          generatedVideo.filename || 'dwellreel-video.mp4'
                        }
                      >
                        <Icon name="download" size={17} />
                        Download MP4
                      </a>
                    )}

                    <div className="storyboard-meta">
                      <span>
                        <Icon name="image" size={15} />
                        {selectedImages.length} photos added
                      </span>

                      <span>9:16 · Vertical</span>
                    </div>

                    <div className="storyboard-track">
                      {[0, 1, 2, 3].map((item) => (
                        <div
                          className={`storyboard-frame ${
                            selectedImages[item] ? 'has-image' : ''
                          }`}
                          key={item}
                        >
                          {selectedImages[item] && (
                            <img
                              src={selectedImages[item].url}
                              alt={`Storyboard preview ${item + 1}`}
                            />
                          )}

                          <span>{String(item + 1).padStart(2, '0')}</span>
                        </div>
                      ))}
                    </div>

                    <p className="preview-footnote">
                      {generatedVideo
                        ? 'Your MP4 has been generated by DwellReel AI.'
                        : storyboard
                          ? `${storyboard.scene_count} scenes generated from your property details.`
                          : 'Preview updates as you add property details and photos.'}
                    </p>
                  </div>

                  <div className="trust-card">
                    <div className="trust-icon">
                      <Icon name="sparkle" size={19} />
                    </div>

                    <div>
                      <strong>Facts first. Always.</strong>

                      <p>
                        Your reel should reflect the real property. Captions
                        are based on the information you provide.
                      </p>
                    </div>
                  </div>
                </aside>
              </form>
            </section>
          ) : (
            /* OVERVIEW DASHBOARD */

            <section className="dashboard-page">
              <div className="welcome-row">
                <div>
                  <div className="eyebrow">
                    <span className="eyebrow-line" />
                    YOUR CREATIVE SPACE
                  </div>

                  <h1>
                    Good stories <span>move people.</span>
                  </h1>

                  <p>
                    Let's make your next property impossible to scroll past.
                  </p>
                </div>

                <button className="primary-button" onClick={openCreator}>
                  <Icon name="plus" size={18} />
                  Create a property reel
                </button>
              </div>

              <section className="hero-banner">
                <div className="hero-copy">
                  <div className="hero-badge">
                    <Icon name="sparkle" size={14} />
                    INTRODUCING YOUR CREATIVE STUDIO
                  </div>

                  <h2>
                    From property photos
                    <br />
                    to <span>powerful stories.</span>
                  </h2>

                  <p>
                    Turn the details that matter into a property video that
                    feels as special as the place itself.
                  </p>

                  <button className="hero-button" onClick={openCreator}>
                    Create your first reel <Icon name="arrow" size={16} />
                  </button>

                  <div className="hero-caption">
                    <span className="caption-dot" />
                    No editing skills needed
                  </div>
                </div>

                <div className="hero-visual">
                  <div className="hero-photo hero-photo-back">
                    <img
                      src="https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=700&q=85"
                      alt="Modern property interior"
                    />
                  </div>

                  <div className="hero-photo hero-photo-front">
                    <img src={SAMPLE_IMAGE} alt="Contemporary house exterior" />

                    <div className="photo-gradient" />

                    <div className="floating-video-card">
                      <span className="mini-play">
                        <Icon name="play" size={13} />
                      </span>

                      <span>
                        <strong>YOUR NEXT LISTING</strong>
                        <small>Made to make an impression.</small>
                      </span>
                    </div>

                    <span className="photo-tag">PROPERTY FILM · 9:16</span>
                  </div>

                  <div className="hero-stamp">
                    <Icon name="sparkle" size={19} />

                    <span>
                      MADE FOR
                      <br />
                      THE WAY WE
                      <br />
                      <b>DISCOVER</b>
                    </span>
                  </div>
                </div>
              </section>

              <section className="steps-section">
                <div className="section-title-row">
                  <div>
                    <span className="eyebrow">THREE SIMPLE STEPS</span>
                    <h2>From listing to living story.</h2>
                  </div>

                  <span className="muted-note">Simple by design.</span>
                </div>

                <div className="steps-grid">
                  <article className="step-card">
                    <span className="step-index">01</span>

                    <div className="step-icon step-icon-lilac">
                      <Icon name="image" size={21} />
                    </div>

                    <h3>Bring the property</h3>
                    <p>
                      Add details and 4–8 photos that show its personality.
                    </p>

                    <span className="step-arrow">
                      <Icon name="arrow" size={16} />
                    </span>
                  </article>

                  <article className="step-card">
                    <span className="step-index">02</span>

                    <div className="step-icon step-icon-peach">
                      <Icon name="microphone" size={21} />
                    </div>

                    <h3>Give it a voice</h3>
                    <p>
                      Add AI narration and background music to bring your
                      property story to life.
                    </p>

                    <span className="step-arrow">
                      <Icon name="arrow" size={16} />
                    </span>
                  </article>

                  <article className="step-card">
                    <span className="step-index">03</span>

                    <div className="step-icon step-icon-green">
                      <Icon name="video" size={21} />
                    </div>

                    <h3>Share the reel</h3>
                    <p>
                      Generate a vertical property video ready to download.
                    </p>

                    <span className="step-arrow">
                      <Icon name="arrow" size={16} />
                    </span>
                  </article>
                </div>
              </section>

              <section className="projects-section">
                <div className="section-title-row">
                  <div>
                    <span className="eyebrow">
                      {activeNav === 'My projects'
                        ? 'YOUR WORKSPACE'
                        : 'A LITTLE INSPIRATION'}
                    </span>

                    <h2>
                      {activeNav === 'My projects'
                        ? 'Your projects'
                        : 'Stories worth a second look.'}
                    </h2>
                  </div>

                  {activeNav !== 'My projects' && (
                    <button
                      className="text-link"
                      onClick={() => setActiveNav('My projects')}
                    >
                      View all <Icon name="arrow" size={15} />
                    </button>
                  )}
                </div>

                {visibleProjects.length === 0 ? (
                  <div className="empty-projects">
                    <div className="empty-icon">
                      <Icon name="folder" size={25} />
                    </div>

                    <h3>Your project space awaits.</h3>

                    <p>
                      Generate and save your first property video to see it
                      here.
                    </p>

                    <button className="primary-button" onClick={openCreator}>
                      <Icon name="plus" size={17} />
                      Create a reel
                    </button>
                  </div>
                ) : (
                  <div className="projects-grid">
                    {visibleProjects.map((project) => (
                      <article className="project-card" key={project.id}>
                        <div className="project-image">
                          <img
                            src={project.image}
                            alt={project.name}
                            loading="lazy"
                          />

                          <span className="project-status">
                            {project.status}
                          </span>

                          <button
                            className="project-play"
                            onClick={() => openSavedProject(project)}
                            aria-label={`View ${project.name}`}
                          >
                            <Icon name="play" size={17} />
                          </button>

                          <span className="project-duration">
                            {project.duration}
                          </span>
                        </div>

                        <div className="project-info">
                          <h3>{project.name}</h3>
                          <p>{project.location}</p>

                          <div className="project-footer">
                            <span>
                              <Icon name="clock" size={14} />

                              {project.status === 'Sample'
                                ? 'Example reel'
                                : project.status}
                            </span>

                            <button onClick={openCreator}>
                              Create something similar{' '}
                              <Icon name="arrow" size={14} />
                            </button>
                          </div>
                        </div>
                      </article>
                    ))}
                  </div>
                )}
              </section>

              <footer className="page-footer">
                <span>DWELLREEL AI</span>
                <span>Every property has a story. Tell yours well.</span>
                <span>Made for the places that matter.</span>
              </footer>
            </section>
          )}
        </div>
      </main>
    </div>
  )
}

function formatDuration(totalSeconds = 0) {
  const seconds = Math.max(0, Number(totalSeconds) || 0)
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.floor(seconds % 60)

  return `${String(minutes).padStart(2, '0')}:${String(
    remainingSeconds
  ).padStart(2, '0')}`
}

export default App