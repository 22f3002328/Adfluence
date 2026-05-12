document.getElementById('return').onclick = function(){
    const baseURL = 'http://127.0.0.1:5000/dashboard_admin';
    
    const queryparams = {'message' : 'null'};
    const searchParams = new URLSearchParams(queryparams);
    
    const url = new URL(`${baseURL}?${searchParams.toString()}`);

    window.location.href = url;
};

// -----------------------------

fetch('/data_stats/inf_distr_data')
.then(response => response.json())
.then(data => {
    const ctx_I = document.getElementById('inf_distr_niche').getContext('2d');

    new Chart(ctx_I, {
        type: 'bar',
        data: {
            labels: ['Education', 'Fashion','Finance','Fitness','Gaming','Technology'],
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(255, 0, 0, 0.7)',
                    'rgba(0, 0, 255, 0.7)',
                    'rgba(0, 128, 0, 0.7)',
                    'rgba(255, 255, 0, 0.7)',
                    'rgba(255, 165, 0, 0.7)',
                    'rgba(255, 192, 203, 0.7)'
                ],
                borderColor: ['white'],
                borderWidth : 1
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Influencer count',
                        font: {
                        size: 14,
                        },
                    }
                },
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Influencer niche',
                        font: {
                        size: 14,
                        },
                    }
                }
            },
            plugins: {
                legend: {
                    display: false, 
                },
                title: {
                    display: true,
                    text: 'Influencer count across niches',
                    font: {family: 'cursive',size: 18,weight: 'bold'}
                }
            }
        }
    })
});

// -----------------------------

fetch('/data_stats/flagged_infs_data')
.then(response => response.json())
.then(data => {
    const ctx_IV = document.getElementById('flagged_infs_distr').getContext('2d');

    new Chart(ctx_IV, {
        type: 'pie',
        data: {
            labels: ['Unflagged','Flagged'],
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(0, 0, 255, 0.7)',
                    'rgba(255, 0, 0, 0.7)'
                ],
                borderColor: ['white'],
                borderWidth : 1
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'left',
                    font: {family: 'cursive',size: 20,weight: 'bold'}
                },
                title: {
                    display: true,
                    text: 'Flagged influencers distribution',
                    font: {family: 'cursive',size: 22,weight: 'bold'}
                },
            }
        }
    })
});

// -----------------------------

fetch('/data_stats/spn_distr_data')
.then(response => response.json())
.then(data => {
    const ctx_II = document.getElementById('spn_distr_industry').getContext('2d');

    new Chart(ctx_II, {
        type: 'bar',
        data: {
            labels: ['Education', 'Fashion','Finance','Fitness','Gaming','Technology'],
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(255, 0, 0, 0.7)',
                    'rgba(0, 0, 255, 0.7)',
                    'rgba(0, 128, 0, 0.7)',
                    'rgba(255, 255, 0, 0.7)',
                    'rgba(255, 165, 0, 0.7)',
                    'rgba(255, 192, 203, 0.7)'
                ],
                borderColor: ['white'],
                borderWidth : 1
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Sponsor count',
                        font: {
                        size: 15
                        },
                    }
                },
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Sponsor industry',
                        font: {
                        size: 15
                        },
                    }
                }
            },
            plugins: {
                legend: {
                    display: false, 
                },
                title: {
                    display: true,
                    text: 'Sponsor count across industries',
                    font: {family: 'cursive',size: 18,weight: 'bold'}
                }
            }
        }
    })
});

// -----------------------------

fetch('/data_stats/flagged_spns_data')
.then(response => response.json())
.then(data => {
    const ctx_III = document.getElementById('flagged_spns_distr').getContext('2d');

    new Chart(ctx_III, {
        type: 'pie',
        data: {
            labels: ['Unflagged','Flagged'],
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(0, 0, 255, 0.7)',
                    'rgba(255, 0, 0, 0.7)'
                ],
                borderColor: ['white'],
                borderWidth : 1
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'left',
                    font: {family: 'cursive',size: 20,weight: 'bold'}
                },
                title: {
                    display: true,
                    text: 'Flagged sponsors distribution',
                    font: {family: 'cursive',size: 22,weight: 'bold'}
                },
            }
        }
    })
});

// -----------------------------

fetch('/data_stats/req_distr_data')
.then(response => response.json())
.then(data => {
    const ctx_I = document.getElementById('req_distr_field').getContext('2d');

    new Chart(ctx_I, {
        type: 'bar',
        data: {
            labels: ['Education', 'Fashion','Finance','Fitness','Gaming','Technology'],
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(255, 0, 0, 0.7)',
                    'rgba(0, 0, 255, 0.7)',
                    'rgba(0, 128, 0, 0.7)',
                    'rgba(255, 255, 0, 0.7)',
                    'rgba(255, 165, 0, 0.7)',
                    'rgba(255, 192, 203, 0.7)'
                ],
                borderColor: ['white'],
                borderWidth : 1
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Request count',
                        font: {
                        size: 14,
                        },
                    }
                },
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Campaign field',
                        font: {
                        size: 14,
                        },
                    }
                }
            },
            plugins: {
                legend: {
                    display: false, 
                },
                title: {
                    display: true,
                    text: 'Advertisement requests count across fields',
                    font: {family: 'cursive',size: 18,weight: 'bold'}
                }
            }
        }
    })
});

// -----------------------------

fetch('/data_stats/flagged_reqs_data')
.then(response => response.json())
.then(data => {
    const ctx_IV = document.getElementById('flagged_reqs_distr').getContext('2d');

    new Chart(ctx_IV, {
        type: 'pie',
        data: {
            labels: ['Unflagged','Flagged'],
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(0, 0, 255, 0.7)',
                    'rgba(255, 0, 0, 0.7)'
                ],
                borderColor: ['white'],
                borderWidth : 1
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'left',
                    font: {family: 'cursive',size: 20,weight: 'bold'}
                },
                title: {
                    display: true,
                    text: 'Flagged requests distribution',
                    font: {family: 'cursive',size: 22,weight: 'bold'}
                },
            }
        }
    })
});

// -----------------------------

fetch('/data_stats/camp_distr_data')
.then(response => response.json())
.then(data => {
    const ctx_I = document.getElementById('camp_distr_field').getContext('2d');

    new Chart(ctx_I, {
        type: 'bar',
        data: {
            labels: ['Education', 'Fashion','Finance','Fitness','Gaming','Technology'],
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(255, 0, 0, 0.7)',
                    'rgba(0, 0, 255, 0.7)',
                    'rgba(0, 128, 0, 0.7)',
                    'rgba(255, 255, 0, 0.7)',
                    'rgba(255, 165, 0, 0.7)',
                    'rgba(255, 192, 203, 0.7)'
                ],
                borderColor: ['white'],
                borderWidth : 1
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Campaign count',
                        font: {
                        size: 14,
                        },
                    }
                },
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Campaign field',
                        font: {
                        size: 14,
                        },
                    }
                }
            },
            plugins: {
                legend: {
                    display: false, 
                },
                title: {
                    display: true,
                    text: 'Campaign count across fields',
                    font: {family: 'cursive',size: 18,weight: 'bold'}
                }
            }
        }
    })
});

// -----------------------------

fetch('/data_stats/flagged_camps_data')
.then(response => response.json())
.then(data => {
    const ctx_IV = document.getElementById('flagged_camps_distr').getContext('2d');

    new Chart(ctx_IV, {
        type: 'pie',
        data: {
            labels: ['Unflagged','Flagged'],
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(0, 0, 255, 0.7)',
                    'rgba(255, 0, 0, 0.7)'
                ],
                borderColor: ['white'],
                borderWidth : 1
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'left',
                    font: {family: 'cursive',size: 20,weight: 'bold'}
                },
                title: {
                    display: true,
                    text: 'Flagged campaigns distribution',
                    font: {family: 'cursive',size: 22,weight: 'bold'}
                },
            }
        }
    })
});