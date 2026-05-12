document.getElementById('return').onclick = function(){
    const campaign_id = document.getElementById('campaign_id').getAttribute('placeholder')
    if(campaign_id.startsWith('pbl')){
        const baseURL = 'http://127.0.0.1:5000/public_requests';
        const queryParams = {'campaign_id' : campaign_id};
    
        const searchParams = new URLSearchParams(queryParams);
        const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
        window.location.href = url;
    }
    else if(campaign_id.startsWith('pvt')){
        window.location.href = 'http://127.0.0.1:5000/pvt_requests';
    }
    
};

document.getElementById('submit').onclick = function(){
    const campaign_id = document.getElementById('campaign_id').getAttribute('placeholder')
    const request_id = document.getElementById('request_id').getAttribute('placeholder')
    const sponsor_id = document.getElementById('sponsor_id').getAttribute('placeholder')
    const desired_amount = document.getElementById('desired_amount').value
    
    const baseURL = 'http://127.0.0.1:5000/negotiate';
    const queryParams = {'campaign_id' : campaign_id,'request_id' : `${request_id}`,'sponsor_id' : `${sponsor_id}`,'desired_amount' : `${desired_amount}`};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;
};