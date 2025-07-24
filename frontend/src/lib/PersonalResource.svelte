<script>
  // Props
  let { token = '' } = $props();

  // Reactive state variables
  let message = $state('');
  let message2 = $state('');
  let timeLeft = $state('');
  let isExpired = $state(false);
  let createdAt = $state('');
  let expiresAt = $state('');
  let secretInfo = $state('')
  let intervalId;

  /**
   * Decode JWT payload
   */
  function decodeJWT(token) {
    try {
      const base64Payload = token.split('.')[1]
        .replace(/-/g, '+')
        .replace(/_/g, '/');
      const jsonPayload = atob(base64Payload);
      return JSON.parse(jsonPayload);
    } catch (err) {
      return null;
    }
  }

  /**
   * Convert seconds to "xh ym zs" format
   */
  function formatSeconds(seconds) {
    if (seconds <= 0) return 'Expired';
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    return [
      hours && `${hours}h`,
      minutes && `${minutes}m`,
      `${secs}s`
    ].filter(Boolean).join(' ');
  }

  /**
   * Main timer function to check token expiry
   */
  function updateTimer() {
    const payload = decodeJWT(token);
    if (!payload) return;

    const nowInSeconds = Math.floor(Date.now() / 1000);
    const { iat, exp } = payload;
    const secondsRemaining = exp - nowInSeconds;

    // Update UI variables
    createdAt = new Date(iat * 1000).toLocaleString();
    expiresAt = new Date(exp * 1000).toLocaleString();
    timeLeft = formatSeconds(secondsRemaining);
    isExpired = secondsRemaining <= 0;

    // Stop timer if expired
    if (isExpired && intervalId) {
      clearInterval(intervalId);
      intervalId = null;
      message = '';
    }
  }

  /**
   * Start countdown when token is available
   */
  $effect(() => {
    if (token) {
      updateTimer(); // Run once immediately
      intervalId = setInterval(updateTimer, 1000); // Update every second
    }

    // Cleanup when component is destroyed
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  });


  /**
   * Call protected API using the JWT
   */
  async function fetchProtected() {
    console.log(`In fetch protected\nand token: ${token}`)
    try {
      const res = await fetch('http://localhost:5000/resources/protected', {
        credentials: "include",
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      message = `${data.message}\nsecret_id: ${data.secret_id}`;
      console.log(`Protected data fetched: ${parseFloat(data.secret_id)}`);
    } catch (err) {
      message = '❌ Failed to fetch protected data.';
    }
  }
</script>

<svelte:head>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    html, body {
      height: 100%;
      overflow: hidden;
    }
  </style>
</svelte:head>

<div class="protected-container">
    <!-- <h1>This is token section </h1> -->
  <div class="protected-card">
    <div class="avatar-container">
      <div class="avatar">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>

    <div class="protected-content">
      <h2>Protected Route</h2>

      {#if token}
        <div class="token-info">
          <h3>JWT Token Info</h3>
          <p><strong>Created:</strong> {createdAt}</p>
          <p><strong>Expires:</strong> {expiresAt}</p>
          <p><strong>Time Left:</strong>
            <span class="time-left" class:expired={isExpired} class:warning={timeLeft.includes('m') || timeLeft.includes('h')}>
              {timeLeft}
            </span>
          </p>
        </div>
      {/if}

      <!-- <button class="fetch-button" onclick={fetchProtected} disabled={isExpired}> -->
      <button class="fetch-button" onclick={fetchProtected}>
        Fetch Protected Data
      </button>

      {#if message}
        <div class="message {message.includes('✅') ? 'success' : 'error'}">
          {message}
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes pulse {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
  }

  @keyframes shimmer {
    0% {
      background-position: -200px 0;
    }
    100% {
      background-position: 200px 0;
    }
  }

  .protected-container {
    height: 100vh;
    width: 100vw;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    position: fixed;
    top: 0;
    left: 0;
  }

  .protected-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 40px 35px;
    width: 100%;
    max-width: 380px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    animation: fadeIn 0.8s ease-out;
  }

  .avatar-container {
    display: flex;
    justify-content: center;
    margin-bottom: 40px;
  }

  .avatar {
    width: 80px;
    height: 80px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.8);
    animation: pulse 3s ease-in-out infinite;
  }

  .protected-content {
    display: flex;
    flex-direction: column;
    gap: 24px;
    color: white;
  }

  h2 {
    font-size: 24px;
    font-weight: 600;
    text-align: center;
    color: white;
  }

  .token-info {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 20px;
    font-size: 14px;
  }

  .token-info h3 {
    font-size: 18px;
    margin-bottom: 16px;
    color: rgba(255, 255, 255, 0.9);
  }

  .token-info p {
    margin: 8px 0;
    color: rgba(255, 255, 255, 0.8);
  }

  .time-left {
    font-weight: bold;
  }

  .time-left.expired {
    color: #f44336;
  }

  .time-left.warning {
    color: #ffa500;
  }

  .time-left:not(.expired):not(.warning) {
    color: #4caf50;
  }

  .fetch-button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 16px 20px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 16px;
    letter-spacing: 1px;
    position: relative;
    overflow: hidden;
  }

  .fetch-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.5s;
  }

  .fetch-button:hover::before {
    left: 100%;
  }

  .fetch-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  }

  .fetch-button:active {
    transform: translateY(0);
  }

  .fetch-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .message {
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    text-align: center;
    animation: fadeIn 0.5s ease-out;
  }

  .message.success {
    background: rgba(28, 161, 37, 0.753);
    color: #012001;
    border: 1px solid rgba(76, 175, 80, 0.3);
  }

  .message.error {
    background: rgba(244, 67, 54, 0.86);
    color: #3d0602;
    border: 1px solid rgba(244, 67, 54, 0.3);
  }

  /* Responsive design */
  @media (max-width: 480px) {
    .protected-card {
      padding: 30px 25px;
      margin: 10px;
    }
  }
</style>