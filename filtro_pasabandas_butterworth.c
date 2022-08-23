int main ( void ) {   
    
    //bandpass filter, fs=50hz
    float n_h[7]   = {0.138006833304702,-0.324553140102072,0.235112835325392,-2.451493822247775e-16,-0.235112835325391,0.324553140102072,-0.138006833304702};
    float d_h[7]   = {1,-4.128299870544583,7.128205555481988,-6.725145142176070,3.703551352217406,-1.102731108338750,0.124421488259499};
    float s_out2[7]; //
        
    
    
    void bp_filter(float _n_h[], float _d_h[], unsigned int _s_in[], float _s_out2[], unsigned int aux_val){
            _s_in[6] = _s_in[5];
            _s_in[5] = _s_in[4];
            _s_in[4] = _s_in[3];
            _s_in[3] = _s_in[2];
            _s_in[2] = _s_in[1];
            _s_in[1] = _s_in[0];
            _s_in[0] = aux_val;
            _s_out2[6] = _s_out2[5];
            _s_out2[5] = _s_out2[4];
            _s_out2[4] = _s_out2[3];
            _s_out2[3] = _s_out2[2];
            _s_out2[2] = _s_out2[1]; //valor 2 veces anterior de la senal PPG
            _s_out2[1] = _s_out2[0]; //valor anterior de la senal ppg
            //valor actual de la senal PPG:
            _s_out2[0] = _n_h[0]*_s_in[0] + _n_h[1]*_s_in[1] + _n_h[2]*_s_in[2] + _n_h[3]*_s_in[3] + _n_h[4]*_s_in[4] + _n_h[5]*_s_in[5] + _n_h[6]*_s_in[6] - _d_h[1]*_s_out2[1] - _d_h[2]*_s_out2[2] - _d_h[3]*_s_out2[3] - _d_h[4]*_s_out2[4] - _d_h[5]*_s_out2[5] - _d_h[6]*_s_out2[6];
            return;
    }
    
    return 0;
}
