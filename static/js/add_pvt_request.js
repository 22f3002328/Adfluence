document.getElementById('return').onclick = function(){
    const campaign_id = document.getElementById('campaign_id').getAttribute('placeholder')
    
    const baseURL = 'http://127.0.0.1:5000/add_request';
    const queryParams = {'campaign_id' : campaign_id}

    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);

    window.location.href = url;
}

document.getElementById('submit').onclick = function(){
    const influencer_id = document.getElementById('influencer_id').getAttribute('placeholder')
    const campaign_id = document.getElementById('campaign_id').getAttribute('placeholder')
    const requirements = document.getElementById('requirements').value
    const payment_amount = document.getElementById('payment_amount').value
    const additional_notes = document.getElementById('additional_notes').value
    

    const baseURL = 'http://127.0.0.1:5000/add_request';
    const queryParams = {'influencer_id': influencer_id,'campaign_id' : campaign_id,'requirements' : requirements,'payment_amount' : payment_amount,'additional_notes' : additional_notes};
    
    const searchParams = new URLSearchParams(queryParams);
    const url = new URL(`${baseURL}?${searchParams.toString()}`);
    
    window.location.href = url;
}