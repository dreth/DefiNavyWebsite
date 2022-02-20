// import jsons data for categories/chains
$.getJSON('/assets/data/categories.json', function(categories_chains) {
    // CREATE CHAIN SELECTOR
    // available chains with this kind of dapp
    var availableChains = categories_chains[$('special').prop('id')].map(obj => {
        return obj['chain']
    });

    // Generate chain selector
    var chainSelector = '<h3 class="inline">Select Chain: </h3>&emsp;<select id="chainSelect" class="largerText">'
    for (var i = 0; i < availableChains.length; i++) {
        chainSelector += `<option value="${availableChains[i]}">${availableChains[i]}</option>`
    }
    chainSelector += '</select>'
    document.getElementById('chainSelector').innerHTML = chainSelector;

    // add onchange event listener to select
    document.getElementById('chainSelect').addEventListener('change', (event) => {
        generateAuditStatusSelector()
        updateProtocols()
    })

    // update audit status selector
    function generateAuditStatusSelector() {
            // CREATE AUDITED STATUS SELECTOR
            // get possible audit statuses
            var auditOptions = ['All'];
            
            // get current chain selection object
            var chainSelection = categories_chains[$('special').prop('id')].filter((item) => {
                return item.chain == $('#chainSelect').val();
            })[0]

            // add elements to audit options selector depending on the chainselection
            if (chainSelection['has_audited'] & chainSelection['has_unaudited'] == false) {
                auditOptions.push('Audited')
            } else if (chainSelection['has_unaudited'] & chainSelection['has_audited'] == false) {
                auditOptions.push('Unaudited')
            } else if (chainSelection['has_unaudited'] & chainSelection['has_audited']) {
                auditOptions.push('Audited')
                auditOptions.push('Unaudited')
            }

            // Generate audit status selector
            var auditSelector = '<h3 class="inline">Select Audit status: </h3>&emsp;<select id="auditSelect" class="largerText">'
            for (var i = 0; i < auditOptions.length; i++) {
                if (auditOptions[i] == 'All') {
                    auditSelector += `<option value="2">${auditOptions[i]}</option>`
                } else if (auditOptions[i] == 'Audited') {
                    auditSelector += `<option value="1">${auditOptions[i]}</option>`
                } else if (auditOptions[i] == 'Unaudited') {
                    auditSelector += `<option value="0">${auditOptions[i]}</option>`
                }
                
            }
            auditSelector += '</select>'

            // show audit links checkbox
            auditSelector += '&nbsp;&nbsp;|<label><input type="checkbox" id="showAuditCheckbox" value="1"> Show audit link</label>'

            document.getElementById('auditSelector').innerHTML = auditSelector;

            // add onchange event listener to select
            document.getElementById('auditSelect').addEventListener('change', (event) => updateProtocols())

            // add onchange event listener to showAuditCheckbox
            document.getElementById('showAuditCheckbox').addEventListener('change', (event) => updateProtocols())
    }



    // update protocols list function
    function updateProtocols() {
        // use protocols data and filter it with the selectors values
        $.getJSON('/assets/data/protocols.json', function(protocols) {
            var data = protocols['protocols'].filter( (o) => {
                // check audit status and act accordingly to apply filters correctly
                let selectedAuditStatus = $('#auditSelect').val();

                // audit status ifelse, 2 is All, 1 is Audited and 0 is Unaudited
                if (selectedAuditStatus == 2) {
                    return o.category == $('special').prop('id') &&
                        o.chains.includes($("#chainSelect").val())
                } else if (selectedAuditStatus == 1) {
                    return o.category == $('special').prop('id') &&
                        o.chains.includes($("#chainSelect").val()) &&
                        o.is_audited == true 
                } else if (selectedAuditStatus == 0) {
                    return o.category == $('special').prop('id') &&
                        o.chains.includes($("#chainSelect").val()) &&
                        o.is_audited == false
                }
            })
            
            // Generate links
            linksGenerated = '<ul>'
            for (var i = 0; i < data.length; i++) {
                if ($('#showAuditCheckbox').is(":checked")) {
                    if (data[i]['is_audited']) {
                        linksGenerated += `<li><a href="${data[i]['url']}" target="_blank">${data[i]['name']}</a>&ensp;-&ensp;`
                        for (var k = 0; k < data[i]['audits'].length; k++) {
                            linksGenerated += `<a href="${data[i]['audits'][k]}" target="_blank" class="auditLinks">(a)</a>&ensp;`
                        }
                        linksGenerated += '</li>'
                    } else {
                        linksGenerated += `<li><a href="${data[i]['url']}" target="_blank">${data[i]['name']}</a></li>`
                    }
                } else {
                    linksGenerated += `<li><a href="${data[i]['url']}" target="_blank">${data[i]['name']}</a></li>`
                }
                

            }
            linksGenerated += '</ul>'

            // append links to div
            document.getElementById('linksGenerationArea').innerHTML = linksGenerated;
        })

    }

    // update the protocols initially
    generateAuditStatusSelector()
    updateProtocols()
})





