<script>
    import { getProfile, login, logout, readTokenFromCookie } from './lib/api.js';

    import PersonalResource from './lib/PersonalResource.svelte';

    let token = $state('');
    let user = $state(null);

    async function init() {
        user = await getProfile();
        if (user) console.log(`User is: ${user.name}`);
    }

    async function handleLogout() {
        const ok = await logout();
        if (ok) user = null;
    }

    async function readToken(){
        token = await readTokenFromCookie();
        if (token) {
            console.log(`Token read: ${token}`);
        } else {
            console.log('No token found');
        }
    }

    init();
</script>

<main>
    {#if user}
        <h1>Welcome {user.name}!</h1>
        <p>Email: {user.email}</p>
        <button onclick={handleLogout}>Logout</button>
        <button onclick={readToken}>Read Token</button>
        {#if token}
            <PersonalResource {token} />
        {:else}
            <p>No token available. Please log in.</p>
        {/if}
    {:else}
        <button onclick={login}>Login with Google</button>
    {/if}
</main>
