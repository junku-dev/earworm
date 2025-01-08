(function (){
    const rpHtml: HTMLElement = document.getElementById('recently-played');
    const topHtml: HTMLElement = document.getElementById('');
    const api_url: string = import.meta.env.PUBLIC_API_URL;
    const url_key: string = import.meta.env.PUBLIC_KEY;

    interface RecentlyPlayedData {
        link: string;
        popularity: number;
        played_at: string;
    }

    function handleError(error: string): void{
        console.error(error);
        rpHtml.innerHTML = `something went wrong...`;
    }

    async function getServerKey(url: string): Promise<void>{
        const req: RequestInit = {
            method:'GET',
            headers: {
                'Accept' : 'application/json',
                'Content-Type': 'application/json'
            },
        };

        await fetch(url, req)
        .then(response => response.json())
        .then(data => {
            const key: string = data['key'];
            getRecentlyPlayed(key)
        })
        .catch(handleError)
    }

    function getRecentlyPlayed(key: string): void{
        const rec: string =`${api_url}/${key}/recents`
        const req: RequestInit = {
            method: 'GET',
            headers:{
                'Accept' : 'application/json',
                'Content-Type': 'application/json'
            }
        }
        fetch(rec, req)
        .then(async (response) => {
            if (response.ok){
                return await response.json();
            }
            else {
                throw await response.json();
            }
        })
        .then((data: RecentlyPlayedData) => {
            rpHtml.innerHTML = displayData(data);
        })
        .catch((error: string) => {
            handleError(error);
        })
    }

    function displayData(data: RecentlyPlayedData): string{
        console.log(data);
        const urlArr: string[] = data['link'].split("/");
        const trackId: string = urlArr[urlArr.length - 1];
        const pop: number = data.popularity
        const timePlayed: string = data.played_at;

        return `
            <iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/${trackId}?utm_source=generator" width="80%" height="152" frameBorder="0" allowfullscreen="" loading="lazy"></iframe>
            <p>track popularity: ${pop}/100</p>
            <p>last played: ${timePlayed}</p>
        `;
    }

    getServerKey(url_key);
})();