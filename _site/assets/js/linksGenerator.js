// import jsons data
$.getJSON('/assets/data/categories.json', function(categories_chains) {
    // available chains with this kind of dapp
    var availableChains = categories_chains[$('special').prop('id')]['chains'];

    // Generate selector
    var chainSelector = '<h3 class="inline">Select Chain: </h3>&emsp;<select id="chainSelect" class="largerText">'
    for (var i = 0; i < availableChains.length; i++) {
        chainSelector += `<option value="${availableChains[i]}">${availableChains[i]}</option>`
    }
    chainSelector += '</select>'
    document.getElementById('chainSelector').innerHTML = chainSelector;

})

fetch('/assets/data/chains_protocols.json').then(response => {
    return response.json();
}).then(chains => {

    function updateProtocols() {
        // selected chain
        var selectedChainProtocolIDs = chains[$("#chainSelect").prop('value')]['ids'];

        // protocols
        $.getJSON('/assets/data/protocols.json', function(protocols) {

            // var protocolsKeys = Object.keys(protocols).filter(item => );

            // Generate selector
            linksGenerated = '<ul>'
            for (const protocol of selectedChainProtocolIDs) {
                if (protocols[protocol]['category'] == $('special').prop('id')) {
                    linksGenerated += `<li><a href="${protocols[protocol]['url']}" target="_blank">${protocols[protocol]['name']}</a></li>`
                }
            }
            linksGenerated += '</ul>'
            
            // append links to div
            document.getElementById('linksGenerationArea').innerHTML = linksGenerated;
        })
    }

    // update the protocols initially
    updateProtocols()

    // add onchange event listener to select
    document.getElementById('chainSelect').addEventListener('change', (event) => updateProtocols())

})



    