<script>
    import { getProfile, login, logout, readTokenFromCookie } from './lib/api.js';

    import PersonalResource from './lib/PersonalResource.svelte';

    let token = $state('');
    let user = $state(null);

    async function init() {
        user = await getProfile();
        // token = await readTokenFromCookie();
    }

    async function handleLogout() {
        const ok = await logout();
        if (ok) user = null;
    }

    async function readToken(){
        token = await readTokenFromCookie();
        if (token) {
            // console.log(`Token read: ${token}`);
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
        <p>Family Name: {user.family_name}</p>
        <button onclick={handleLogout}>Logout</button>
        <button onclick={readToken}>Load Token</button>
        {#if token}
            <PersonalResource {token} />
        {:else}
            <p>Token is available for next {user.jwt_time_period}. Quickly load the token for <strong>protected resource access</strong>.</p>
        {/if}
    {:else}
        <button onclick={login}>Login with Google</button>
    {/if}

</main>