let nodeCounter = 0;
const nodes = [];

function addNode(event) {
    event.preventDefault();
    const target = event.target;
    const parentNode = target.parentElement;
    if (!parentNode) {
        console.error("Parent node not found.");
        return;
    }
    const parentID = parentNode.dataset.id;
    let ul = parentNode.querySelector('ul');
    if (!ul) {
        ul = document.createElement("ul");
        parentNode.appendChild(ul);
    }
    let nextID = 0;
    const existingNodes = document.querySelectorAll('[data-id]');
    let li = document.createElement("li");
    nextID += existingNodes.length;

    // Append new node to the end of the list
    ul.appendChild(li);

    const a = document.createElement("a");
    a.href = "#";
    if (nextID === 0) {
        a.textContent = "Root";
    } else {
        a.textContent = "Node " + nextID;
    }
    a.onclick = addNode;
    li.appendChild(a);
    const addButton = document.createElement('button');
    addButton.textContent = '+';
    addButton.className = 'add-btn';
    addButton.onclick = addNode;
    li.appendChild(addButton);
    li.dataset.id = nextID;
    nodes.push({ id: nextID, parent_id: parentID, name: a.textContent });

    // Add drag and drop area
    const dragDropContainer = document.createElement('div');
    dragDropContainer.id = "drop-area";
    dragDropContainer.style.cssText = "border: 2px dashed black; width: 320px; height: 240px;";
    dragDropContainer.innerHTML = '<p>Drag and drop videos here</p>';

    dragDropContainer.addEventListener('drag', drag);

    dragDropContainer.addEventListener('drop', drop);

    li.appendChild(dragDropContainer);
}

function drag(event) {
    event.dataTransfer.setData("text", event.target.innerHTML);
}

function drop(event) {
    event.preventDefault();
    var data = event.dataTransfer.getData("text");
    event.target.innerHTML = data;
    var video = event.target.querySelector('video');
    if (video) {
        video.width = 320; // Set the width to match other videos
        video.height = 240; // Set the height to match other videos
        var source = video.querySelector('source');
        var src = source.getAttribute('src');
        var filename = src.substring(src.lastIndexOf('/') + 1);
        fetch('/save_video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: filename })
        })
            .then(response => response.text())
            .then(data => console.log(data))
            .catch(error => console.error(error));
    }
}

function collectTreeData() {
    nodes.length = 0;
    
    const rootElement = document.getElementById("tree-root");
    if (rootElement) {
        traverse(rootElement);
        nodes.sort((a, b) => (a.id > b.id) ? 1 : ((b.id > a.id) ? -1 : 0));
    } else {
        console.error("Root element not found.");
    }
    return nodes;
}


function updateTree() {
    // document.getElementById('update-btn').textContent = con.eid;
    const id = li.dataset.id;
    const treeData = collectTreeData();
    fetch('/update_tree', {
        
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nodes: treeData })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text || 'Failed to update tree') });
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error updating tree:', error);
    });
}

const traversedNodes = new Set();

function traverse(node) {
    const liElements = node.querySelectorAll('li');
    console.log(`Traversing node: ${node.dataset.id}`); // Debug: Log current node being traversed
    liElements.forEach(function (li) {
        const id = li.dataset.id;
        if (traversedNodes.has(id)) {
            return;
        }
        traversedNodes.add(id);
        const name = li.querySelector('a').textContent;
        if (id === '0') {
            return;
        }
        const parentNode = li.parentElement.closest('li');
        const parentNodeID = parentNode ? parentNode.dataset.id : '0';
        nodes.push({ id: id, parent_id: parentNodeID, name: name });
        console.log(`Added node: ${id}, parent_id: ${parentNodeID}, name: ${name}`); // Debug: Log node addition
        const ul = li.querySelector('ul');
        
        if (ul) {
            traverse(ul);
        } else {
            console.log(`No further ul found in li with id: ${id}`); // Debug: Log end of branch
        }
    });
}

function loadTree() {
    fetch('/get_tree_data')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch tree data');
            }
            return response.json();
        })
        .then(data => {
            const rootElement = document.getElementById("tree-root");
            if (rootElement) {
                rootElement.innerHTML = '';
                if (data.nodes && data.nodes.length > 0) {
                    data.nodes.forEach(node => {
                        const li = document.createElement("li");
                        li.dataset.id = node.id;
                        const a = document.createElement("a");
                        a.href = "#";
                        a.textContent = node.name;
                        a.onclick = addNode;
                        li.appendChild(a);
                        const parentNode = rootElement.querySelector(`[data-id="${node.parent_id}"]`);
                        if (parentNode) {
                            let ul = parentNode.querySelector("ul");
                            if (!ul) {
                                ul = document.createElement("ul");
                                parentNode.appendChild(ul);
                            }
                            ul.appendChild(li);
                        } else {
                            rootElement.appendChild(li);
                        }
                        if (!node.has_children) {
                            const addButton = document.createElement('button');
                            addButton.textContent = '+';
                            addButton.className = 'add-btn';
                            addButton.onclick = addNode;
                            li.appendChild(addButton);
                        }
                    
                        // Add drag and drop area
                        const dragDropContainer = document.createElement('div');
                        dragDropContainer.id = "drop-area";
                        dragDropContainer.style.cssText = "border: 2px dashed black; width: 320px; height: 240px;";
                        dragDropContainer.innerHTML = '<p>Drag and drop videos here</p>';
                        dragDropContainer.addEventListener('dragover', function (e) {
                            e.preventDefault();
                        });
                        dragDropContainer.addEventListener('drop', function (e) {
                            e.preventDefault();
                            var data = e.dataTransfer.getData("text");
                            e.target.innerHTML = data;
                            var video = e.target.querySelector('video');
                        if (video) {
                            video.width = 320; // Set the width to match other videos
                            video.height = 240; // Set the height to match other videos
                            var source = video.querySelector('source');
                            var src = source.getAttribute('src');
                            var filename = src.substring(src.lastIndexOf('/') + 1);
                            fetch('/save_video', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                    },
                                body: JSON.stringify({ filename: filename })
                            })
                            .then(response => response.text())
                            .then(data => console.log(data))
                            .catch(error => console.error(error));
                        }
                        });
                        li.appendChild(dragDropContainer);
                    
                        // Add form for "Add Hotspot"
                        const form = document.createElement("form");
                        form.action = "/hotspot";
                        form.method = "GET";
                        const hiddenInput = document.createElement("input");
                        hiddenInput.type = "hidden";
                        hiddenInput.name = "eid";
                        hiddenInput.id = "eid";
                        hiddenInput.value = "{{con.eid}}"; // Ensure this template string is correctly replaced in your actual application context
                        const button = document.createElement("button");
                        button.type = "submit";
                        button.className = "btn";
                        button.textContent = "Add Hotspot";
                        form.appendChild(button);
                        form.appendChild(hiddenInput);
                        li.appendChild(form);
                    });
                } else {
                    const li = document.createElement("li");
                    li.dataset.id = 0;
                    const a = document.createElement("a");
                    a.href = "#";
                    a.textContent = "Root (0)";
                    a.onclick = addNode;
                    li.appendChild(a);
                    li.style.alignItems = 'center';
                    li.style.alignItems = 'center';
                    const form = document.createElement("form");
                    form.action = "/hotspot";
                    form.method = "GET";
                    const hiddenInput = document.createElement("input");
                    hiddenInput.type = "hidden";
                    hiddenInput.name = "eid";
                    hiddenInput.id = "eid";
                    hiddenInput.value = "{{con.eid}}";
                    const button = document.createElement("button");
                    button.type = "submit";
                    button.className = "btn";
                    button.textContent = "Add Hotspot";
                    form.appendChild(button);
                    form.appendChild(hiddenInput);
                    const dragDropContainer = document.createElement('div');
                    dragDropContainer.id = "drop-area";
                    dragDropContainer.style.cssText = "border: 2px dashed black; width: 320px; height: 240px;";
                    dragDropContainer.innerHTML = '<p>Drag and drop videos here</p>';
                    dragDropContainer.addEventListener('dragover', function (e) {
                        e.preventDefault();
                    });
                    dragDropContainer.addEventListener('drop', function (e) {
                        e.preventDefault();
                        var data = e.dataTransfer.getData("text");
                        e.target.innerHTML = data;
                        var video = e.target.querySelector('video');
                    if (video) {
                        video.width = 320; // Set the width to match other videos
                        video.height = 240; // Set the height to match other videos
                        var source = video.querySelector('source');
                        var src = source.getAttribute('src');
                        var filename = src.substring(src.lastIndexOf('/') + 1);
                        fetch('/save_video', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                                },
                            body: JSON.stringify({ filename: filename })
                        })
                        .then(response => response.text())
                        .then(data => console.log(data))
                        .catch(error => console.error(error));
                    }
                    });
                    
                    li.appendChild(dragDropContainer);
                    li.insertBefore(form, dragDropContainer);
                    rootElement.appendChild(li);
                }
            } else {
                console.error("Root element not found.");
            }
        })
        .catch(error => {
            console.error('Error loading tree:', error);
        });
}

window.addEventListener('load', loadTree);

const updateBtn = document.getElementById("update-btn");
if (updateBtn) {
    updateBtn.addEventListener("click", updateTree);
} else {
    console.error("Update button element not found.");
}
 function drop(event) {
            event.preventDefault();
            var data = event.dataTransfer.getData("text");
            event.target.innerHTML = data;
            var video = event.target.querySelector('video');
            if (video) {
                video.width = 320; // Set the width to match other videos
                video.height = 240; // Set the height to match other videos
                var source = video.querySelector('source');
                var src = source.getAttribute('src');
                var filename = src.substring(src.lastIndexOf('/') + 1);
                fetch('/save_video', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ filename: filename })
                })
                .then(response => response.text())
                .then(data => console.log(data))
                .catch(error => console.error(error));
            }
        }