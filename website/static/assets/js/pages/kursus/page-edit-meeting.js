Vue.createApp({
    data() {
        return {
            form: {
                uuid: null,
                title: null,
                video: null,
                material: '',
            },
            uuid: null,
            editor: null,
            csrf: token
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        const currentUrl = window.location.href
        const urlPats = currentUrl.split('/')
        this.uuid = urlPats[urlPats.length - 2]
        this.form.uuid = urlPats[urlPats.length - 1]

        this.getDetail()
    },
    methods: {
        quillInitial(){
            this.editor = new Quill('#snow-editor', {
                bounds: '#snow-editor',
                placeholder: 'Tulis materi nya di sini yaa..',
                modules: {
                  formula: true,
                  toolbar: '#snow-toolbar'
                },
                theme: 'snow'
            })
            this.editor.root.innerHTML = this.form.material
            this.editor.on('text-change', () => {
                this.form.material = this.editor.root.innerHTML
            });
        },
        async onSubmit(){
            $.blockUI({
                message: '<div class="spinner-border text-white" role="status"></div>',
                css: {
                    backgroundColor: 'transparent',
                    border: '0'
                },
                overlayCSS: {
                    opacity: 0.5
                }
            })

            await axios.post(`/courses/${this.uuid}/${this.form.uuid}/submit`, this.form, { 
                headers: { "X-CSRFToken": this.csrf }
            })
            .then(response => {
                $.unblockUI()
                Swal.fire({
                    icon: "success",
                    text: response.data.success,
                    timer: 2000,
                    showConfirmButton: false,
                }).then(() => {
                    location.href = `/courses/${this.uuid}`
                })
            })
            .catch(error => {
                $.unblockUI()
                Swal.fire({
                    icon: "error",
                    text: error.response.data.error,
                    timer: 2000,
                    showConfirmButton: false,
                })
            })
        },
        async getDetail(){
            $.blockUI({
                message: '<div class="spinner-border text-white" role="status"></div>',
                css: {
                    backgroundColor: 'transparent',
                    border: '0'
                },
                overlayCSS: {
                    opacity: 0.5
                }
            })

            await axios.get(`/courses/${this.uuid}/${this.form.uuid}/get-data`)
                .then(result => {
                    $.unblockUI()
                    var data = result.data
                    this.form.title = data.title
                    this.form.video = data.video
                    this.form.material = data.material
                    this.quillInitial()
                })
                .catch(() => {
                    $.unblockUI();
                    Swal.fire({
                        icon: "warning",
                        text: "Gagal mengambil data!",
                        timer: 2000,
                        showConfirmButton: false,
                    })
                })
        },
    }
}).mount('#app')