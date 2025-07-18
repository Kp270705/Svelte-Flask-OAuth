<script>
    let user = null;

    async function fetchProfile() {
        const res = await fetch("http://localhost:5000/profile", {
            credentials: "include"
        });
        if (res.ok) {
            user = await res.json();
        }
    }

    function login() {
        window.location.href = "http://localhost:5000/login";
    }

    async function logout() {
        const res = await fetch("http://localhost:5000/logout", {
            credentials: "include"
        });
        if (res.ok) {
            user = null;
        }
    }

    fetchProfile();
</script>

<main>
    {#if user}
        <h1>Welcome {user.name}!</h1>
        <p>Email: {user.email}</p>
        <button on:click={logout}>Logout</button>
    {:else}
        <button on:click={login}>Login with Google</button>
    {/if}
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 4rem;
    }

    button {
        margin-top: 1rem;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        cursor: pointer;
    }
</style>
