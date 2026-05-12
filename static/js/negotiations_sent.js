document.getElementById('return').onclick = function(){
    const baseURL = 'http://127.0.0.1:5000/dashboard_influencer';
    const queryParams = {'message' : 'null'};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;
}