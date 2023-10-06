class standard_deviation:
    def __init__(self):
        self.points_curr = []
        self.points_7 = []
        self.points_15 = []
        self.points_30 = []
        self.points_prev = []
        self.points_proj = []
        self.points_prevProj = []
        self.points_avg_curr = []
        self.points_avg_7 = []
        self.points_avg_15 = []
        self.points_avg_30 = []
        self.points_avg_prev = []
        self.points_avg_proj = []
        self.points_avg_prevProj = []
        self.blocks_curr = []
        self.blocks_7 = []
        self.blocks_15 = []
        self.blocks_30 = []
        self.blocks_prev = []
        self.blocks_proj = []
        self.blocks_prevProj = []
        self.blocks_avg_curr = []
        self.blocks_avg_7 = []
        self.blocks_avg_15 = []
        self.blocks_avg_30 = []
        self.blocks_avg_prev = []
        self.blocks_avg_proj = []
        self.blocks_avg_prevProj = []
        self.assists_curr = []

        self.assists_7 = []
        self.assists_15 = []
        self.assists_30 = []
        self.assists_prev = []
        self.assists_proj = []
        self.assists_prevProj = []
        self.assists_avg_curr = []
        self.assists_avg_7 = []
        self.assists_avg_15 = []
        self.assists_avg_30 = []
        self.assists_avg_prev = []
        self.assists_avg_proj = []
        self.assists_avg_prevProj = []
        self.rebounds_curr = []
        self.rebounds_7 = []
        self.rebounds_15 = []
        self.rebounds_30 = []
        self.rebounds_prev = []
        self.rebounds_proj = []
        self.rebounds_prevProj = []
        self.rebounds_avg_curr = []
        self.rebounds_avg_7 = []
        self.rebounds_avg_15 = []
        self.rebounds_avg_30 = []
        self.rebounds_avg_prev = []
        self.rebounds_avg_proj = []
        self.rebounds_avg_prevProj = []
        self.steals_curr = []
        self.steals_7 = []
        self.steals_15 = []
        self.steals_30 = []
        self.steals_prev = []
        self.steals_proj = []
        self.steals_prevProj = []
        self.steals_avg_curr = []
        self.steals_avg_7 = []
        self.steals_avg_15 = []
        self.steals_avg_30 = []
        self.steals_avg_prev = []
        self.steals_avg_proj = []
        self.steals_avg_prevProj = []
        self.turnovers_curr = []
        self.turnovers_7 = []
        self.turnovers_15 = []
        self.turnovers_30 = []
        self.turnovers_prev = []
        self.turnovers_proj = []
        self.turnovers_prevProj = []
        self.turnovers_avg_curr = []
        self.turnovers_avg_7 = []
        self.turnovers_avg_15 = []
        self.turnovers_avg_30 = []
        self.turnovers_avg_prev = []
        self.turnovers_avg_proj = []

        self.turnovers_avg_prevProj = []
        self.fga_curr = []
        self.fga_7 = []
        self.fga_15 = []
        self.fga_30 = []
        self.fga_prev = []
        self.fga_proj = []
        self.fga_prevProj = []
        self.fga_avg_curr = []
        self.fga_avg_7 = []
        self.fga_avg_15 = []
        self.fga_avg_30 = []
        self.fga_avg_prev = []
        self.fga_avg_proj = []
        self.fga_avg_prevProj = []
        self.fgm_curr = []
        self.fgm_7 = []
        self.fgm_15 = []
        self.fgm_30 = []
        self.fgm_prev = []
        self.fgm_proj = []
        self.fgm_prevProj = []
        self.fgm_avg_curr = []
        self.fgm_avg_7 = []
        self.fgm_avg_15 = []
        self.fgm_avg_30 = []
        self.fgm_avg_prev = []
        self.fgm_avg_proj = []
        self.fgm_avg_prevProj = []
        self.fgp_curr = []
        self.fgp_7 = []
        self.fgp_15 = []
        self.fgp_30 = []
        self.fgp_prev = []
        self.fgp_proj = []
        self.fgp_prevProj = []
        self.fgp_avg_curr = []
        self.fgp_avg_7 = []
        self.fgp_avg_15 = []
        self.fgp_avg_30 = []
        self.fgp_avg_prev = []
        self.fgp_avg_proj = []
        self.fgp_avg_prevProj = []
        self.fta_curr = []
        self.fta_7 = []
        self.fta_15 = []
        self.fta_30 = []
        self.fta_prev = []
        self.fta_proj = []
        self.fta_prevProj = []
        self.fta_avg_curr = []
        self.fta_avg_7 = []
        self.fta_avg_15 = []

        self.fta_avg_30 = []
        self.fta_avg_prev = []
        self.fta_avg_proj = []
        self.fta_avg_prevProj = []
        self.ftm_curr = []
        self.ftm_7 = []
        self.ftm_15 = []
        self.ftm_30 = []
        self.ftm_prev = []
        self.ftm_proj = []
        self.ftm_prevProj = []
        self.ftm_avg_curr = []
        self.ftm_avg_7 = []
        self.ftm_avg_15 = []
        self.ftm_avg_30 = []
        self.ftm_avg_prev = []
        self.ftm_avg_proj = []
        self.ftm_avg_prevProj = []
        self.ftp_curr = []
        self.ftp_7 = []
        self.ftp_15 = []
        self.ftp_30 = []
        self.ftp_prev = []
        self.ftp_proj = []
        self.ftp_prevProj = []
        self.ftp_avg_curr = []
        self.ftp_avg_7 = []
        self.ftp_avg_15 = []
        self.ftp_avg_30 = []
        self.ftp_avg_prev = []
        self.ftp_avg_proj = []
        self.ftp_avg_prevProj = []
        self.tpm_curr = []
        self.tpm_7 = []
        self.tpm_15 = []
        self.tpm_30 = []
        self.tpm_prev = []
        self.tpm_proj = []
        self.tpm_prevProj = []
        self.tpm_avg_curr = []
        self.tpm_avg_7 = []
        self.tpm_avg_15 = []
        self.tpm_avg_30 = []
        self.tpm_avg_prev = []
        self.tpm_avg_proj = []
        self.tpm_avg_prevProj = []

    def to_dict(self):
        return {
            'points_curr': self.points_curr,
            'points_7': self.points_7,
            'points_15': self.points_15,
            'points_30': self.points_30,
            'points_prev': self.points_prev,
            'points_proj': self.points_proj,
            'points_prevProj': self.points_prevProj,
            'points_avg_curr': self.points_avg_curr,
            'points_avg_7': self.points_avg_7,
            'points_avg_15': self.points_avg_15,
            'points_avg_30': self.points_avg_30,
            'points_avg_prev': self.points_avg_prev,
            'points_avg_proj': self.points_avg_proj,
            'points_avg_prevProj': self.points_avg_prevProj,
            'blocks_curr': self.blocks_curr,
            'blocks_7': self.blocks_7,
            'blocks_15': self.blocks_15,
            'blocks_30': self.blocks_30,
            'blocks_prev': self.blocks_prev,
            'blocks_proj': self.blocks_proj,
            'blocks_prevProj': self.blocks_prevProj,
            'blocks_avg_curr': self.blocks_avg_curr,
            'blocks_avg_7': self.blocks_avg_7,
            'blocks_avg_15': self.blocks_avg_15,
            'blocks_avg_30': self.blocks_avg_30,
            'blocks_avg_prev': self.blocks_avg_prev,
            'blocks_avg_proj': self.blocks_avg_proj,
            'blocks_avg_prevProj': self.blocks_avg_prevProj,
            'assists_curr': self.assists_curr,
            'assists_7': self.assists_7,
            'assists_15': self.assists_15,
            'assists_30': self.assists_30,
            'assists_prev': self.assists_prev,
            'assists_proj': self.assists_proj,
            'assists_prevProj': self.assists_prevProj,
            'assists_avg_curr': self.assists_avg_curr,
            'assists_avg_7': self.assists_avg_7,
            'assists_avg_15': self.assists_avg_15,
            'assists_avg_30': self.assists_avg_30,
            'assists_avg_prev': self.assists_avg_prev,
            'assists_avg_proj': self.assists_avg_proj,
            'assists_avg_prevProj': self.assists_avg_prevProj,
            'rebounds_curr': self.rebounds_curr,
            'rebounds_7': self.rebounds_7,
            'rebounds_15': self.rebounds_15,
            'rebounds_30': self.rebounds_30,
            'rebounds_prev': self.rebounds_prev,
            'rebounds_proj': self.rebounds_proj,
            'rebounds_prevProj': self.rebounds_prevProj,
            'rebounds_avg_curr': self.rebounds_avg_curr,
            'rebounds_avg_7': self.rebounds_avg_7,
            'rebounds_avg_15': self.rebounds_avg_15,
            'rebounds_avg_30': self.rebounds_avg_30,
            'rebounds_avg_prev': self.rebounds_avg_prev,
            'rebounds_avg_proj': self.rebounds_avg_proj,
            'rebounds_avg_prevProj': self.rebounds_avg_prevProj,
            'steals_curr': self.steals_curr,
            'steals_7': self.steals_7,
            'steals_15': self.steals_15,
            'steals_30': self.steals_30,
            'steals_prev': self.steals_prev,
            'steals_proj': self.steals_proj,
            'steals_prevProj': self.steals_prevProj,
            'steals_avg_curr': self.steals_avg_curr,
            'steals_avg_7': self.steals_avg_7,
            'steals_avg_15': self.steals_avg_15,
            'steals_avg_30': self.steals_avg_30,
            'steals_avg_prev': self.steals_avg_prev,
            'steals_avg_proj': self.steals_avg_proj,
            'steals_avg_prevProj': self.steals_avg_prevProj,
            'turnovers_curr': self.turnovers_curr,
            'turnovers_7': self.turnovers_7,
            'turnovers_15': self.turnovers_15,
            'turnovers_30': self.turnovers_30,
            'turnovers_prev': self.turnovers_prev,
            'turnovers_proj': self.turnovers_proj,
            'turnovers_prevProj': self.turnovers_prevProj,
            'turnovers_avg_curr': self.turnovers_avg_curr,
            'turnovers_avg_7': self.turnovers_avg_7,
            'turnovers_avg_15': self.turnovers_avg_15,
            'turnovers_avg_30': self.turnovers_avg_30,
            'turnovers_avg_prev': self.turnovers_avg_prev,
            'turnovers_avg_proj': self.turnovers_avg_proj,
            'turnovers_avg_prevProj': self.turnovers_avg_prevProj,
            'fga_curr': self.fga_curr,
            'fga_7': self.fga_7,
            'fga_15': self.fga_15,
            'fga_30': self.fga_30,
            'fga_prev': self.fga_prev,
            'fga_proj': self.fga_proj,
            'fga_prevProj': self.fga_prevProj,
            'fga_avg_curr': self.fga_avg_curr,
            'fga_avg_7': self.fga_avg_7,
            'fga_avg_15': self.fga_avg_15,
            'fga_avg_30': self.fga_avg_30,
            'fga_avg_prev': self.fga_avg_prev,
            'fga_avg_proj': self.fga_avg_proj,
            'fga_avg_prevProj': self.fga_avg_prevProj,
            'fgm_curr': self.fgm_curr,
            'fgm_7': self.fgm_7,
            'fgm_15': self.fgm_15,
            'fgm_30': self.fgm_30,
            'fgm_prev': self.fgm_prev,
            'fgm_proj': self.fgm_proj,
            'fgm_prevProj': self.fgm_prevProj,
            'fgm_avg_curr': self.fgm_avg_curr,
            'fgm_avg_7': self.fgm_avg_7,
            'fgm_avg_15': self.fgm_avg_15,
            'fgm_avg_30': self.fgm_avg_30,
            'fgm_avg_prev': self.fgm_avg_prev,
            'fgm_avg_proj': self.fgm_avg_proj,
            'fgm_avg_prevProj': self.fgm_avg_prevProj,
            'fgp_curr': self.fgp_curr,
            'fgp_7': self.fgp_7,
            'fgp_15': self.fgp_15,
            'fgp_30': self.fgp_30,
            'fgp_prev': self.fgp_prev,
            'fgp_proj': self.fgp_proj,
            'fgp_prevProj': self.fgp_prevProj,
            'fgp_avg_curr': self.fgp_avg_curr,
            'fgp_avg_7': self.fgp_avg_7,
            'fgp_avg_15': self.fgp_avg_15,
            'fgp_avg_30': self.fgp_avg_30,
            'fgp_avg_prev': self.fgp_avg_prev,
            'fgp_avg_proj': self.fgp_avg_proj,
            'fgp_avg_prevProj': self.fgp_avg_prevProj,
            'fta_curr': self.fta_curr,
            'fta_7': self.fta_7,
            'fta_15': self.fta_15,
            'fta_30': self.fta_30,
            'fta_prev': self.fta_prev,
            'fta_proj': self.fta_proj,
            'fta_prevProj': self.fta_prevProj,
            'fta_avg_curr': self.fta_avg_curr,
            'fta_avg_7': self.fta_avg_7,
            'fta_avg_15': self.fta_avg_15,
            'fta_avg_30': self.fta_avg_30,
            'fta_avg_prev': self.fta_avg_prev,
            'fta_avg_proj': self.fta_avg_proj,
            'fta_avg_prevProj': self.fta_avg_prevProj,
            'ftm_curr': self.ftm_curr,
            'ftm_7': self.ftm_7,
            'ftm_15': self.ftm_15,
            'ftm_30': self.ftm_30,
            'ftm_prev': self.ftm_prev,
            'ftm_proj': self.ftm_proj,
            'ftm_prevProj': self.ftm_prevProj,
            'ftm_avg_curr': self.ftm_avg_curr,
            'ftm_avg_7': self.ftm_avg_7,
            'ftm_avg_15': self.ftm_avg_15,
            'ftm_avg_30': self.ftm_avg_30,
            'ftm_avg_prev': self.ftm_avg_prev,
            'ftm_avg_proj': self.ftm_avg_proj,
            'ftm_avg_prevProj': self.ftm_avg_prevProj,
            'ftp_curr': self.ftp_curr,
            'ftp_7': self.ftp_7,
            'ftp_15': self.ftp_15,
            'ftp_30': self.ftp_30,
            'ftp_prev': self.ftp_prev,
            'ftp_proj': self.ftp_proj,
            'ftp_prevProj': self.ftp_prevProj,
            'ftp_avg_curr': self.ftp_avg_curr,
            'ftp_avg_7': self.ftp_avg_7,
            'ftp_avg_15': self.ftp_avg_15,
            'ftp_avg_30': self.ftp_avg_30,
            'ftp_avg_prev': self.ftp_avg_prev,
            'ftp_avg_proj': self.ftp_avg_proj,
            'ftp_avg_prevProj': self.ftp_avg_prevProj,
            'tpm_curr': self.tpm_curr,
            'tpm_7': self.tpm_7,
            'tpm_15': self.tpm_15,
            'tpm_30': self.tpm_30,
            'tpm_prev': self.tpm_prev,
            'tpm_proj': self.tpm_proj,
            'tpm_prevProj': self.tpm_prevProj,
            'tpm_avg_curr': self.tpm_avg_curr,
            'tpm_avg_7': self.tpm_avg_7,
            'tpm_avg_15': self.tpm_avg_15,
            'tpm_avg_30': self.tpm_avg_30,
            'tpm_avg_prev': self.tpm_avg_prev,
            'tpm_avg_proj': self.tpm_avg_proj,
            'tpm_avg_prevProj': self.tpm_avg_prevProj,
        }
