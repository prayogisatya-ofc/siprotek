Vue.createApp({
    data() {
        return {
            csrf: token,
            qrCodeScanner: null,
            isScanning: true,
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        this.qrCodeScanner = new Html5QrcodeScanner(
            "reader", { fps: 10, qrbox: 250 });
        this.qrCodeScanner.render(this.onScanSuccess);
    },
    methods: {
        async onScanSuccess(qrCodeMessage){
            if(this.isScanning){

                this.isScanning = false;

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
    
                try {
                    const response = await axios.post(`/scanqr/submit`, {kode: qrCodeMessage}, {
                        headers: { "X-CSRFToken": this.csrf }
                    });
        
                    $.unblockUI();
                    Swal.fire({
                        icon: "success",
                        text: response.data.success,
                        timer: 4000,
                        showConfirmButton: false,
                    });
                } catch (error) {
                    $.unblockUI();
                    Swal.fire({
                        icon: "warning",
                        text: error.response.data.error,
                        timer: 2000,
                        showConfirmButton: false,
                    });
                }

                setTimeout(() => {
                    this.isScanning = true;
                }, 5000);
            }
        }
    }
}).mount('#app')