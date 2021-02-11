document.querySelectorAll('.like-dislike-btn').forEach(opinionButton => {
    opinionButton.addEventListener('click', () => {
        var id = opinionButton.id
        var opinionType = id.split('-')[0]
        var productId = id.split('-')[1]

        if (opinionType === 'dislike' || opinionType === 'like') {
            $.ajax({
                'url': '/like-dislike/',
                'type': 'post',
                'data': {
                    'action': opinionType,
                    'product-id': productId,
                },
                'beforeSend': function(xhr) {
                    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
                },
                'success': function(data) {
                    var error = data['errors']
                    var liked = data['liked']
                    var disliked = data['disliked']

                    if (error) {
                        document.getElementById('alert-box').style.display = 'block'
                        document.getElementById('alert-box').innerText = error
                        setTimeout(() => {
                            document.getElementById('alert-box').innerText = ''
                            document.getElementById('alert-box').style.display = 'none'
                        }, 5000)
                    }

                    var likeId = 'like-'+productId
                    var dislikeId = 'dislike-'+productId
                    switch (liked) {
                        case 'true':
                            document.getElementById(likeId).classList.add('btn-acted')
                            break
                        case 'false':
                            document.getElementById(likeId).classList.remove('btn-acted')
                            break
                    }

                    switch (disliked) {
                        case 'true':
                            document.getElementById(dislikeId).classList.add('btn-acted')
                            break
                        case 'false':
                            document.getElementById(dislikeId).classList.remove('btn-acted')
                    }
                }
            })
        }
    })
})
