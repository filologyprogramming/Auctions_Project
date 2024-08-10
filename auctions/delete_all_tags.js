// Delete all tags in listings
                let parent_nodes = document.getElementsByClassName("a");
                if (parent_nodes != null) {
                    parent_nodes.forEach (parent => {
                        // Define children
                        let children = parent.children;
                        for (let i = children.length - 1; i >= 0; i--) {
                            children[i].remove();
                        }
                    })
                }