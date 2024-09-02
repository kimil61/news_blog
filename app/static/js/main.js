document.addEventListener('DOMContentLoaded', function () {
    const tagInput = document.getElementById('tag-input');
    const tagSuggestions = document.getElementById('tag-suggestions');
    const selectedTags = document.getElementById('selected-tags');
    const form = document.querySelector('form');

    if (tagInput) {
        tagInput.addEventListener('input', debounce(function () {
            const query = this.value;
            if (query.length > 1) {
                fetch(`/api/search_tags?q=${query}`)
                    .then(response => response.json())
                    .then(tags => {
                        tagSuggestions.innerHTML = '';
                        tags.forEach(tag => {
                            const div = document.createElement('div');
                            div.textContent = tag.name;
                            div.classList.add('cursor-pointer', 'p-2', 'hover:bg-gray-200');
                            div.addEventListener('click', () => addTag(tag));
                            tagSuggestions.appendChild(div);
                        });
                    });
            } else {
                tagSuggestions.innerHTML = '';
            }
        }, 300));
    }

    function addTag(tag) {
        const tagElement = document.createElement('span');
        tagElement.textContent = tag.name;
        tagElement.classList.add('bg-blue-500', 'text-white', 'rounded-full', 'px-2', 'py-1', 'm-1');

        const removeButton = document.createElement('button');
        removeButton.textContent = 'x';
        removeButton.classList.add('ml-1', 'font-bold');
        removeButton.addEventListener('click', () => tagElement.remove());

        tagElement.appendChild(removeButton);
        selectedTags.appendChild(tagElement);

        tagInput.value = '';
        tagSuggestions.innerHTML = '';
    }

    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    if (form) {
        form.addEventListener('submit', function (e) {
            const tagInput = document.createElement('input');
            tagInput.type = 'hidden';
            tagInput.name = 'tags';
            tagInput.value = Array.from(selectedTags.children).map(span => span.textContent.slice(0, -1)).join(',');
            this.appendChild(tagInput);
        });
    }
});