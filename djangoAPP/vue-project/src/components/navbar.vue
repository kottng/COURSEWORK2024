<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="background-color: rgba(97, 172, 151, 1);">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">BotanicView</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link rounded" href="{% url 'Plants' %}" onmouseover="this.style.backgroundColor='#217a67';" onmouseout="this.style.backgroundColor='transparent';">Plants</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link rounded" href="{% url 'addPlant' %}" onmouseover="this.style.backgroundColor='#217a67';" onmouseout="this.style.backgroundColor='transparent';">add Plant</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link rounded" href="{% url 'myProfile' %}" onmouseover="this.style.backgroundColor='#217a67';" onmouseout="this.style.backgroundColor='transparent';">my Profile</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link rounded" href="{% url 'register' %}" onmouseover="this.style.backgroundColor='#217a67';" onmouseout="this.style.backgroundColor='transparent';">Register</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link rounded" href="{% url 'my-login' %}" onmouseover="this.style.backgroundColor='#217a67';" onmouseout="this.style.backgroundColor='transparent';">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link rounded" href="{% url 'user-logout' %}" onmouseover="this.style.backgroundColor='#217a67';" onmouseout="this.style.backgroundColor='transparent';">User logout</a>
                    </li>
                </ul>
                <form class="d-flex">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>
</template>

<script>
</script>

<style>
</style>