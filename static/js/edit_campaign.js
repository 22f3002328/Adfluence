document.getElementById('return').onclick = function(){
    const baseURL = 'http://127.0.0.1:5000/dashboard_sponsor';
    const queryParams = {'message' : 'null'};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;
};

document.getElementById('submit').onclick = function(){
    const campaign_id = document.getElementById('campaign_id').textContent.slice(1,8)
    const start_date = document.getElementById('start_date').value
    const end_date = document.getElementById('end_date').value
    const budget = document.getElementById('budget').value
    
    const baseURL = 'http://127.0.0.1:5000/edit_campaign';
    const queryParams = {'campaign_id' : campaign_id,'start_date' : start_date,'end_date' : end_date,'budget' : budget};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;
};